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
#       python3 social_check.py BUILD.html --long   (long play: 280 ship days with a steady stand-in player; the social save
#       must stay within SAVE_MAX at day 140 and under LONG_MAX every four weeks to day 280; the biggest parts are printed.
#       Measure it on a build with social B 0.39.18+)
import sys, json
exec(open(__file__.replace('social_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

LONG = '--long' in sys.argv                # long play: only the save over LONG_DAYS days (about 30 minutes)
if LONG: sys.argv.remove('--long')
DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 14
LONG_DAYS, LONG_MID, LONG_MAX = 280, 140, 40000   # the lead's rule: at most SAVE_MAX at day 140, under LONG_MAX at any length
SAVE_MAX = 30000               # bytes of the save's social part

# run `days` days from Day 1 06:00 hour by hour (or in one jump), with or without the stand-in player
RUN = r"""(({ days, player, jump, notes }) => {
  const h0 = 6, h1 = h0 + days * 24, stats = { born: {}, spread: [] };
  setShipNow(h0 * 60); SHIP_DAYS.clear(); if (typeof machinesNow === 'function') machinesNow();   // an earlier clock: machines afresh
  socInit(); socReset(h0); if (SHIP.device && Array.isArray(SHIP.device.appts)) SHIP.device.appts.length = 0;   // invitations become appointments
  const watch = () => { for (const x of NEWS) stats.born[x.id] = x.kind; };
  // stand-in bus notes (a repair by you and by a crew member, a tradition you came to), each with the time it happened:
  // hour by hour they arrive as they happen; in a jump they all arrive at once, as section 13's bus sends them after a skip
  const oven = typeof machineList === 'function' && machineList().find(x => x.kind === 'oven'), N = notes && oven ? [[h0 * 60 + 200, 'repair', { who: 'you', machine: oven.id, state: 'failing' }],
    [h0 * 60 + 900, 'repair', { who: 'pell', machine: oven.id }], [h0 * 60 + 1500, 'tradition', { id: 'quiz', came: ['tomas', 'pell'], you: true }], [h0 * 60 + 2300, 'repair', { who: 'you', machine: oven.id }]] : [];
  const hear = (a, b) => { for (const [t, k, d] of N) if (t >= a && t < b) socHear(k, { ...d, t }); };
  if (notes) relAdd('tomas', 'chat', 1);
  if (jump) { setShipNow(h1 * 60); hear(-1e9, h1 * 60); socialTo(h1 * 60); watch(); }
  else for (let h = h0 + 1; h <= h1; h++) {
    setShipNow(h * 60); hear((h - 1) * 60, h * 60); socialTo(h * 60); watch();
    for (const x of NEWS) if (h * 60 - x.born >= 720 && h * 60 - x.born < 780) stats.spread.push([x.kind, x.seed.length, SHIP.knows[x.id].size]);
    if (player && h === h0 + 3 * 24 + 6) { memAdd('rina', 'moment.test.1'); memAdd('pell', 'missed.test'); memAdd('pell', 'intro.arrival'); }
    if (player && h % 24 === 12) { relAdd('tomas', 'chat', REL_PTS.chat); memAdd('tomas', 'chat'); if ((h / 24 | 0) % 2) relAdd('pell', 'chat', REL_PTS.chat); for (const x of newsKnownBy('rina')) playerHeard(x.id, 'rina'); }
    if (player && h % 24 === 18) relAdd('tomas', 'meal', REL_PTS.meal);
    if (player && h % 24 === 10 && (h / 24 | 0) % 2 && typeof machineList === 'function') { const m = machineList().find(x => x.kind === 'oven'); if (m) repNote('repair', { who: 'you', machine: m.id }); }   // fixes a galley oven every other day
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
    sample: NEWS.slice(-6).map(x => x.lines[0]), mem: Object.fromEntries(Object.entries(SHIP.mem).map(([k, l]) => [k, l.map(m => m[0] + ' ' + Math.round(m[2]))])), rep: SHIP.rep && { dept: SHIP.rep.dept, ship: SHIP.rep.ship, view: repView() },
    bonds: typeof storyHour === 'function' ? Object.values(SHIP.social.bonds || {}).reduce((o, b) => (o[b.kind] = (o[b.kind] || 0) + 1, o), {}) : null };
})"""

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)

# long play: a steady stand-in player who hears all the news going round each evening and asks everyone they chat to about themselves (on time 9 days in 10, a repair most days, chats to Tomas, Pell, Rina and one more,
# lunch with Tomas, quiz and Tiles night each week) for LONG_DAYS days on paper, story Mail delivered as the game would
LONG_RUN = r"""((days) => {
  const h0 = 6; setShipNow(h0 * 60); SHIP_DAYS.clear(); if (typeof machinesNow === 'function') machinesNow();
  socInit(); socReset(h0); if (SHIP.device && Array.isArray(SHIP.device.appts)) SHIP.device.appts.length = 0;
  const crew = SOC.crew.filter(p => !p.reserve), pal = ['tomas', 'pell', 'rina'], weeks = [];
  const parts = () => { const s = socSave(); return { size: JSON.stringify(s).length, parts: Object.entries(s).map(([k, v]) => [k, JSON.stringify(v).length]).sort((a, b) => b[1] - a[1]).slice(0, 8) }; };
  for (let h = h0 + 1; h <= h0 + days * 24; h++) {
    setShipNow(h * 60); socialTo(h * 60); SHIP.social.mail = SHIP.social.mail.filter(x => x.at > h * 60);   // delivered (socialMail, which the test stops)
    const hr = h % 24, d = Math.floor(h / 24) + 1, u = schedU(d, h, 9001);
    if (hr === 8) repNote('shiftStart', { late: u < .1 ? 25 : 0 });
    if (hr === 12) { for (const id of pal) if (schedU(d, socHash(id), 9002) < .6) { relAdd(id, 'chat', REL_PTS.chat); memAdd(id, 'chat'); }
      const o = crew[Math.floor(schedU(d, h, 9003) * crew.length)]; relAdd(o.id, 'chat', REL_PTS.chat); memAdd(o.id, 'chat');
      for (const q of [o, ...pal.map(id => SOC.crew[SOC.idx.get(id)])]) { const K = relGet(q.id).known, nx = (q.about || []).map(x => x.text).concat(q.life || []).find(x => x && !K.includes(x)); if (nx) K.push(nx); } }   // and asks them about themselves
    if (hr === 13) relAdd('tomas', 'meal', REL_PTS.meal);
    if (hr === 18) for (const x of NEWS.slice()) if (x.born <= h * 60 && x.seed.length) playerHeard(x.id, x.seed[0]);   // a heavy listener: hears everything going round each evening
    if (hr === 10 && typeof machineList === 'function' && u < .7) { const ms = machineList(); repNote('repair', { who: 'you', machine: ms[Math.floor(schedU(d, h, 9004) * ms.length)].id }); }
    if (hr === 20 && (d % 7 === 2 || d % 7 === 5)) repNote('tradition', { id: d % 7 === 2 ? 'quiz' : 'tiles-night', you: true });
    if (hr === 23 && d % 28 === 0) { let r = 0; for (const v of SHIP.aff) if (v <= -40) r++; weeks.push({ day: d, ...parts(), rivals: r }); }
  }
  return weeks;
})"""

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    if LONG:
        g.ev("window.__realTick = tickShip; tickShip = () => {}; socialTick = () => {}")
        lw = g.ev(LONG_RUN + f"({LONG_DAYS})")
        for x in lw: print(f"Day {x['day']}: social save {x['size']} bytes, rivals {x['rivals']}, biggest parts {x['parts']}")
        mid = [x for x in lw if x['day'] == LONG_MID]
        if not mid or mid[0]['size'] > SAVE_MAX: fail(f'the social save is over {SAVE_MAX} bytes at day {LONG_MID}')
        if not lw or lw[-1]['day'] != LONG_DAYS or any(x['size'] >= LONG_MAX for x in lw): fail(f'the social save reaches {LONG_MAX} bytes before day {LONG_DAYS}')
        print('errors', g.errors[:5])
        if g.errors: ok = False
        print('SOCIAL LONG CHECK OK' if ok else 'SOCIAL LONG CHECK FAILED')
        sys.exit(0 if ok else 1)
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

    print('Memories after the run:', json.dumps(a['mem']))
    m = a['mem']
    if not any(x.startswith('chat ') for x in m.get('tomas', [])): fail('Tomas should remember chatting')
    if not any(x.startswith('moment.test.1 ') for x in m.get('rina', [])): fail("Rina's big memory should last two weeks")
    if any(x.startswith('missed.test') for x in m.get('pell', [])): fail("Pell's sour memory should have faded")
    if 'intro.arrival 100' not in m.get('pell', []): fail('a core memory should stay at 100')
    if not any(k != 'rina' and any(x.startswith('heard.moment.test.1') for x in l) for k, l in m.items()): print('  (nobody heard of the big memory: Rina has no friends at 40+)')

    if a.get('bonds') is not None:          # 20c's bonds (social B), once storyHour is in
        bk = a['bonds']; print('Bonds after the run:', json.dumps(bk))
        if not (15 <= bk.get('friends', 0) + bk.get('best', 0) <= 40) or not (2 <= bk.get('rivals', 0) <= 6) or not bk.get('mentor'): print('  NOTE bond numbers outside the plan\'s targets (friends 15-40, rivals 2-6, a mentor)')
    rp = a['rep']
    print('Reputation after the run:', json.dumps(rp and {'dept': rp['dept'], 'ship': rp['ship'], 'knownFor': rp['view']['knownFor']}))
    if not rp or rp['dept']['galley'] < 20 or max(v for k, v in rp['dept'].items() if k not in ('galley', 'works')) >= 20: fail('a stand-in who fixes galley ovens should be known in the galley, and only there')

    # 3. the save: size, and back again
    print(f"Save: social part {a['size']} bytes (limit {SAVE_MAX})")
    if a['size'] > SAVE_MAX: fail('the save is too big')
    rt = g.ev("(() => { const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); return s === JSON.stringify(socSave()); })()")
    mm = g.ev(r"""(() => { for (const x of NEWS) if (x.seed.length) playerHeard(x.id, x.seed[0]); socNote('repair', { who: 'you', kind: 'oven', deck: 3 });   // in memory the same after a save (0.36.75)
      const tp = SOC.crew[SOC.idx.get('tomas')], K = relGet('tomas').known; for (const x of [(tp.about || [])[0] && tp.about[0].text, (tp.life || [])[0], 'news', 'Loves tea'].filter(Boolean)) if (!K.includes(x)) K.push(x);   // known, packed to '#a0' / '#l0' (0.36.76)
      const live = new Set(NEWS.map(x => x.id)), m = () => JSON.stringify([SHIP.social.cues, SHIP.social.pairs, SHIP.heard.filter(h => live.has(h.id)), SHIP.rel.tomas.known]), a = m(), sv = socSave(); socLoad(JSON.parse(JSON.stringify(sv)));
      return [a === m() && sv.rel.tomas[3].some(k => /^#a/.test(k)), SHIP.heard.filter(h => live.has(h.id)).length, SHIP.social.cues.length, Object.keys(SHIP.social.pairs).length]; })()""")
    print('In memory the same after a save (cues, pair news, heard, known):', mm)
    if not mm[0]: fail('a save and load changes cues, pair news, what you heard or what you know')
    print('Save and load give back the same:', rt)
    xl = g.ev(r"""(() => { const s0 = socSave(), A = JSON.stringify(Array.from(SHIP.aff)), R = JSON.stringify(SHIP.rel), Bd = JSON.stringify(SHIP.social.bonds || {});
      const s1 = JSON.parse(JSON.stringify(s0)); s1.ids = 12345; socLoad(s1); const moved = JSON.stringify(Array.from(SHIP.aff)) === A && JSON.stringify(SHIP.rel) === R && JSON.stringify(SHIP.social.bonds) === Bd;
      const s3 = JSON.parse(JSON.stringify(s0)); s3.bonds = JSON.parse(Bd); socLoad(s3); if (JSON.stringify(SHIP.social.bonds) !== Bd) return ['old bond form', Bd.length];
      const s2 = JSON.parse(JSON.stringify(s0)); s2.ids = 12345; delete s2.idl; socLoad(s2); const kept = JSON.stringify(SHIP.rel) === R && NEWS.length === 0;
      socLoad(s0); return [moved, kept]; })()""")
    print('A save from a different crew list: affinity moved across by id, rest kept:', xl)
    rv = g.ev(r"""(() => { relAdd('tomas', 'chat', 12); memAdd('tomas', 'fav.lamp'); repAdd('galley', 5, { work: 3 });
      const s0 = JSON.parse(JSON.stringify(socSave())), R = JSON.stringify(SHIP.rel), M = JSON.stringify(SHIP.mem), P = JSON.stringify(SHIP.rep), A = affinity('tomas', 'pell');
      const t = SOC.crew[SOC.idx.get('tomas')];
      const own = typeof ROSTER_RESERVE !== 'undefined' && Array.isArray(ROSTER_RESERVE), RR = own ? ROSTER_RESERVE : (window.ROSTER_RESERVE = []);   // the game's own reserve when it has one
      RR.push({ ...JSON.parse(JSON.stringify(t)), id: 'reserve-test', name: 'Testy Reserve', seed: 4242, aboard: [400, null] });
      SOC = null; socInit(); const n = SOC.n; socLoad(s0);
      const o = [n === s0.idl.split(',').length + 1 && JSON.stringify(SHIP.social.bonds) === JSON.stringify(bondsUnpack(s0.bonds, s0.idl.split(','))), JSON.stringify(SHIP.rel) === R, JSON.stringify(SHIP.mem) === M, JSON.stringify(SHIP.rep) === P, affinity('tomas', 'pell') === A, affinity('tomas', 'reserve-test') === affStart(t, SOC.crew[SOC.idx.get('reserve-test')])];
      RR.pop(); if (!own) delete window.ROSTER_RESERVE; SOC = null; socInit(); socLoad(s0); return o; })()""")
    print('A reserve person added between save and load (bigger crew, rel, mem, rep, affinity kept, new pair from its start):', rv)
    if rv != [True] * 6: fail('adding a reserve person loses what the save had')
    if xl != [True, True]: fail('a save with a different crew list loses what it should keep')
    if not rt: fail('save and load differ')

    # 4. one jump over two days against the same two days hour by hour (no player)
    c = run(days=2, player=False, jump=False, notes=True)
    d = run(days=2, player=False, jump=True, notes=True)
    print('Two days in one jump the same as hour by hour (with bus notes):', c['key'] == d['key'])
    if c['key'] != d['key']: fail('a time jump gives a different social life')
    if 'fixed.oven' not in c['key'] or 'came.quiz' not in c['key']: fail('the stand-in bus notes left no memories')
    # the same through section 13's real bus, when it's there: the note's shape (its kind and t) as the bus sends it
    bus = g.ev(r"""(() => { if (typeof simNote !== 'function') return null;
      const oven = machineList().find(x => x.kind === 'oven'), keep = JSON.stringify(socSave()), t = Math.floor(shipNow());
      SHIP.mem = {}; SHIP.social.cues = []; relAdd('tomas', 'chat', 1);
      simNote('repair', { who: 'you', machine: oven.id, state: 'failing', kind: 'oven', t }); socialTo(t + 120);
      const o = { cue: !!cue('repair.oven.you'), wrong: !!cue('repair.repair'), mem: Object.values(SHIP.mem).some(l => l.some(m => m[0] === 'fixed.oven')), queued: (SHIP.social.noteq || []).length };
      socLoad(JSON.parse(keep)); return o; })()""")
    print('Through the real bus:', bus)
    if bus is not None and (not bus['cue'] or bus['wrong'] or not bus['mem'] or bus['queued']): fail(f'a repair sent through the bus is read wrongly: {bus}')

    # 5. the query API (0.36.20): what the dialogue engine's line conditions read; pure, and right on a known state
    q = g.ev(r"""(() => {
      const out = {}, works = SOC.crew.find(p => p.dept === 'works' && p.rank !== 'chief'), tomas = SOC.crew[SOC.idx.get('tomas')];
      newsAdd({ id: 'test:one', lines: ['A test.'], seed: ['tomas'], born: Math.floor(shipNow()) - 1 });
      const before = JSON.stringify(socSave());
      out.missing = ['mem', 'warmth', 'affBand', 'bondOf', 'moodOf', 'beatOf', 'knowsNews', 'repBand', 'repShip', 'knownFor', 'cue', 'socialFill', 'memTold', 'inWeek1', 'leavingSoon', 'newHere', 'movedOff', 'memThing'].filter(f => { try { return typeof eval(f) !== 'function'; } catch (e) { return true; } });
      out.band = [affBand('tomas', 'pell'), affinity('tomas', 'pell')];
      out.bandsOk = SOC.crew.slice(0, 20).every(p => SOC.crew.slice(0, 20).every(q => { const v = affinity(p, q), b = affBand(p, q); return b === (v <= -40 ? 'rival' : v >= 60 ? 'friend' : 'neutral'); }));
      out.mood = ['low', 'ok', 'high'].includes(moodOf(tomas)) && moodOf('nobody') === 'ok';
      out.rep = [repBand('works'), repBand('galley'), repShip('work'), knownFor().length];
      out.warm = warmth('tomas');
      const n = NEWS.find(x => SHIP.knows[x.id].size); out.news = n ? [knowsNews([...SHIP.knows[n.id]][0], n.id), knowsNews([...SHIP.knows[n.id]][0], n.id.split(':')[0])] : null;
      out.fill = { me: socialFill(tomas, 'me'), nick: socialFill(tomas, 'nick'), boss: socialFill(works, 'boss'), thing: socialFill(tomas, 'thing', { mem: 'fixed.oven' }), none: socialFill(tomas, 'rival'), fam: socialFill({ ...tomas, family: 'a brother in the Concord navy' }, 'family'), hob: socialFill({ ...tomas, hobby: undefined, habits: ['gardener'] }, 'hobby'), since: socialFill({ ...tomas, since: undefined, aboard: null }, 'since'), grow: socialFill({ ...tomas, since: 'six years', aboard: null }, 'since'), growWant: socDuration(6 * 365 + SHIP.time.day - 1) };
      out.calm = memClass('readyroom.lights') === 'big' && memThing('fixed.oven') === 'the oven' && memThing('nothing') === null && memThing('came.quiz') === 'the quiz night' && memThing('show.pell-show') === 'the music boxes';
      const tz = SOC.crew.find(p => p.thread && /^arc:/.test(p.thread) && p.thread.slice(4) !== p.id); if (tz) { const had = SHIP.rel[tz.id] ? { ...SHIP.rel[tz.id] } : null; relGet(tz.id).arc = 2; out.beatMap = beatOf(tz.thread.slice(4)) === 2; if (had) SHIP.rel[tz.id] = had; else delete SHIP.rel[tz.id]; } else out.beatMap = true;
      out.memNone = mem('tomas', 'fav') === null && bondOf('tomas', 'best') === null;
      const B0 = SHIP.social.bonds; SHIP.social.bonds = { 'tomas:pell': { kind: 'friends', since: 1 }, 'calder:tomas': { kind: 'mentor', since: 1 } };
      out.bonds = [socialFill(tomas, 'friend'), bondOf('tomas', 'friend'), bondOf('pell', 'friends'), socialFill(tomas, 'mentor'), bondOf('calder', 'mentee'), socialFill(tomas, 'best')]; SHIP.social.bonds = B0;
      out.pure = JSON.stringify(socSave()) === before;
      if (!out.pure) { const a = JSON.parse(before), b = socSave(); out.impure = Object.keys({ ...a, ...b }).filter(k => JSON.stringify(a[k]) !== JSON.stringify(b[k])).map(k => k + ': ' + JSON.stringify(a[k]).slice(0, 80) + ' -> ' + JSON.stringify(b[k]).slice(0, 80)); }   // which part changed
      socNote('repair', { who: 'you', kind: 'oven', deck: 3 }); socNote('repair', { who: 'pell', kind: 'fan', deck: 5 });
      out.cue = [!!cue('repair.oven'), !!cue('repair.oven.you'), !!cue('repair.fan'), !!cue('repair.fan.you'), !!cue('repair'), cue('repair.lift') === null];
      const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); out.cueSaved = s === JSON.stringify(socSave()) && !!cue('repair.oven.you');
      setShipNow(shipNow() + 3 * 1440); out.cueGone = cue('repair.oven') === null; setShipNow(shipNow() - 3 * 1440);
      return out;
    })()""")
    print('Query API:', json.dumps(q))
    if q['missing']: fail(f"query functions missing: {q['missing']}")
    if not q.get('calm'): fail('CALM_TYPES or memThing wrong')
    if not q.get('beatMap'): fail('beatOf does not map an arc id to its crew member')
    if q['bonds'] != ['Pell', 'pell', 'tomas', 'Chief Calder', 'tomas', None]: fail(f"bonds and their placeholders wrong: {q['bonds']}")
    if q['news'] != [True, True]: fail(f"knowsNews wrong: {q['news']}")
    if not q['bandsOk'] or not q['mood'] or not q['pure']: fail(f"affBand, moodOf or purity wrong (changed: {q.get('impure')})")
    if q['rep'][:3] != ['new', 'new', 'ok'] : fail(f"repBand/repShip defaults wrong: {q['rep']}")
    if q['news'] and q['news'] != [True, True]: fail(f"knowsNews wrong: {q['news']}")
    if q['fill'].get('fam') != 'a brother in the Concord navy' or q['fill'].get('grow') != q['fill'].get('growWant') or q['fill'].get('hob') != 'gardening' or q['fill'].get('since') is not None: fail(f"theme fill-ins wrong: {q['fill']}")
    if q['fill']['boss'] is None or q['fill']['none'] is not None or q['fill']['thing'] is None: fail(f"socialFill wrong: {q['fill']}")
    if q['cue'] != [True, True, True, False, True, True] or not q['cueSaved'] or not q['cueGone']: fail(f"cues wrong: {q['cue']} saved {q['cueSaved']} gone {q['cueGone']}")

    # 6. memories (0.36.21): adding, refreshing, the ninth pushing out the lightest, fading by half-life, callbacks told once
    r = g.ev(r"""(() => {
      const o = {}; SHIP.mem = {}; const t0 = shipNow();
      memAdd('tomas', 'chat'); memAdd('tomas', 'fav.lamp'); memAdd('tomas', 'chat'); o.refresh = SHIP.mem.tomas.length === 2;
      for (let i = 0; i < 8; i++) memAdd('tomas', 'came.t' + i, { w: 20 + i }); o.max = SHIP.mem.tomas.length; o.kept = !!mem('tomas', 'fav.lamp') && !mem('tomas', 'came.t0');
      o.prefix = mem('tomas', 'fav').key; o.none = mem('tomas', 'fa');
      o.told = [memTold('tomas', 'fav'), mem('tomas', 'fav').told, memTold('tomas', 'fav')];
      o.warm = warmth('tomas');
      SHIP.mem = {}; memAdd('pell', 'chat'); memAdd('pell', 'fixed.oven'); memAdd('pell', 'moment.x'); memAdd('pell', 'intro.arrival'); memAdd('pell', 'grubby');
      const w = () => Object.fromEntries((SHIP.mem.pell || []).map(m => [m[0], Math.round(m[2])]));
      for (let i = 0; i < 7; i++) memFade(); o.week = w();
      for (let i = 0; i < 14; i++) memFade(); o.three = w();
      const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); o.saved = s === JSON.stringify(socSave());
      SHIP.mem = {}; return o;
    })()""")
    print('Memories:', json.dumps(r))
    if not r['refresh'] or r['max'] != 8 or not r['kept']: fail('adding memories wrong (refresh, at most 8, the lightest goes)')
    if r['prefix'] != 'fav.lamp' or r['none'] is not None or r['told'] != [True, True, False]: fail('mem prefix or memTold wrong')
    wk, th = r['week'], r['three']
    near = lambda x, v: x is not None and abs(x - v) <= 1
    if not (near(wk.get('chat'), 15) and near(wk.get('fixed.oven'), 48) and near(wk.get('grubby'), 12) and wk.get('intro.arrival') == 100): fail(f"fading after a week wrong: {wk}")
    if 'chat' in th or 'grubby' in th or not near(th.get('moment.x'), 71) or not near(th.get('fixed.oven'), 30) or th.get('intro.arrival') != 100: fail(f"fading after three weeks wrong: {th}")
    if not r['saved']: fail('memories save and load differ')

    # 7. lines through the dialogue engine (0.36.22): without lineFor, or with one that finds nothing, every card line is
    # as before; with one, chatLine asks it by kind, the new kinds (callback, cue) included
    e = g.ev(r"""(() => {
      const o = {}, crew = SOC.crew.slice(0, 30), t0 = Math.floor(shipNow() / 60) * 60;
      for (const id of ['tomas', 'pell', 'rina']) { relAdd(id, 'chat', 30); relGet(id).arc = 99; }   // no story beats in the way
      const all = () => JSON.stringify(crew.flatMap(p => [0, 1, 2, 3, 4, 5].map(k => chatLine(p, t0 + 60 * k))));
      const realLF = typeof lineFor === 'function' ? lineFor : undefined;   // section 22's, when merged: swapped in the game's own scope, put back after
      lineFor = undefined; const base = all(); lineFor = () => null; o.nullSame = all() === base;
      const asked = {}; lineFor = (p, kind, ctx) => { asked[kind] = (asked[kind] || 0) + 1; return { text: kind + ':' + p.id, id: kind, kind }; };
      memAdd('tomas', 'fav.lamp'); socNote('repair', { who: 'you', kind: 'oven' });
      const kinds = {}; for (const p of SOC.crew) for (let k = 0; k < 6; k++) { const l = chatLine(p, t0 + 60 * k); kinds[l.kind] = (kinds[l.kind] || 0) + 1; }
      o.kinds = kinds; o.asked = asked;
      o.tomas = [0, 1, 2, 3, 4, 5, 6, 7].map(k => chatLine(SOC.crew[SOC.idx.get('tomas')], t0 + 60 * k).kind);
      lineFor = undefined; o.back = all() === base; lineFor = realLF;
      SHIP.mem = {}; SHIP.social.cues = []; return o;
    })()""")
    print('Lines by kind:', json.dumps(e))
    if not e['nullSame'] or not e['back']: fail('card lines change when the dialogue engine finds nothing')
    for k in ('greet', 'near', 'cue'):
        if not e['kinds'].get(k): fail(f'no {k} lines asked of the engine')
    if 'callback' not in e['tomas']: fail("Tomas never calls back the lamp")

    # 8. the first week (0.36.23): gates from onboarding's flags, intro memories, the escort as mentor, socialInvite
    w = g.ev(r"""(() => {
      const o = {}, F = new Set(), had = typeof flag === 'function' ? flag : null; SHIP.mem = {};
      o.open = ['d2', 'd3', 'd5', 'done'].every(socGate);
      const introWas = SHIP.intro; SHIP.intro = { on: true, step: 'arrival', escort: 'torres-zeke', done: {} }; flag = k => F.has(k);   // the game's own flag (section 13) swapped in its scope
      const realLF = typeof lineFor === 'function' ? lineFor : undefined;
      o.shut = ['d2', 'd3', 'd5', 'done'].map(socGate); F.add('week1.d2'); F.add('week1.d3'); o.tue = ['d2', 'd3', 'd5', 'done'].map(socGate);
      socIntroNote({ step: 'arrival', who: ['torres-zeke'] }); socIntroNote({ step: 'dinner', who: [] }); socIntroNote({ step: 'look', who: ['pell'] }); socIntroNote({ step: 'bunk', who: ['rina'], missed: true });
      o.mem = [mem('torres-zeke', 'intro.arrival') && mem('torres-zeke', 'intro.arrival').w, !!mem('calder', 'intro.dinner'), !!mem('pell', 'intro') || !!mem('rina', 'intro')];
      o.mentor = [SHIP.social.mentor, bondOf('torres-zeke', 'mentee'), socialFill(SOC.crew[SOC.idx.get('torres-zeke')], 'mentee')];
      lineFor = (p, kind) => kind === 'week1' ? { text: 'w1', id: 'w1', kind } : null;
      o.week1 = chatLine(SOC.crew[SOC.idx.get('torres-zeke')]).kind;
      F.add('week1.done'); o.done = [socIntroOn(), socGate('done'), chatLine(SOC.crew[SOC.idx.get('torres-zeke')]).kind !== 'week1'];
      lineFor = realLF; SHIP.intro = introWas; flag = had || undefined;
      const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); o.saved = SHIP.social.mentor === 'torres-zeke';
      SHIP.social.mentor = null; SHIP.mem = {};
      // an invitation to a tradition someone is going to
      let hit = null;
      for (let d = 2; d <= 14 && !hit; d++) for (const e of eventsOn(d)) { if (hit) break; for (const p of SOC.crew) { const seg = planDay(p, d).find(x => x.placeId && x.tag && x.tag.startsWith('ev-' + e.id)); if (seg) { hit = { d, id: e.id, p: p.id, seg }; break; } } }
      if (hit) {
        const keep = SHIP.device.appts.slice(), t = shipNow(); setShipNow((hit.d - 1) * 1440 + 360);
        const id = socialInvite({ trad: hit.id, day: hit.d, from: hit.p }), a = SHIP.device.appts.find(x => x.id === id);
        o.invite = { trad: hit.id, day: hit.d, ok: !!a && a.status === 'asked' && a.kind === 'invite' && a.by === hit.p && a.where === hit.seg.placeId && a.at === hit.seg.from,
                     again: socialInvite({ trad: hit.id, day: hit.d, from: hit.p }), none: socialInvite({ trad: 'nothing', day: hit.d, from: hit.p }) };
        SHIP.device.appts.length = 0; SHIP.device.appts.push(...keep); setShipNow(t);
      }
      return o;
    })()""")
    print('First week:', json.dumps(w))
    if not w['open'] or w['shut'] != [False, False, False, False] or w['tue'] != [True, True, False, False]: fail('week-1 gates wrong')
    if w['mem'] != [100, True, False] or w['mentor'][:2] != ['torres-zeke', 'you']: fail(f"intro memories or mentor wrong: {w['mem']} {w['mentor']}")
    if w['week1'] != 'week1' or w['done'] != [False, True, True] or not w['saved']: fail('week-1 lines or the end of week 1 wrong')
    if not w.get('invite') or not w['invite']['ok'] or w['invite']['again'] is not None or w['invite']['none'] is not None: fail(f"socialInvite wrong: {w.get('invite')}")

    # 9. gifts (0.36.24): Give from your hands, how it lands by taste, once a week each, double on a birthday; crew gifts; keepsakes
    gf = g.ev(r"""(() => {
      const o = {}, P = SHIP.player, carry = P.carry.slice(); SHIP.mem = {};
      const open = q => { const v = typeof voiceOf === 'function' ? voiceOf(q.id) : typeof VOICE !== 'undefined' ? VOICE[q.id] : null; return !v || v.openness !== 'guarded'; };   // guarded people gain 20% slower (20c)
      const p = SOC.crew.find(q => giftTaste(q).loves.includes('tea') && open(q)) || SOC.crew.find(q => giftTaste(q).loves.includes('tea')) || SOC.crew[0], t = giftTaste(p);
      const pts0 = relGet(p.id).pts; P.carry = []; o.add = [giftAdd('tin of tea'), giftAdd('a spanner'), giftAdd('herbs'), giftAdd('biscuits')];
      o.hands = giftInHands();
      const a = giftGive(p, 'tin of tea'); o.first = a && a.how; o.pts = Math.round((relGet(p.id).pts - pts0) * 100) / 100; o.mem = mem(p.id, 'gift.tea') && Math.round(mem(p.id, 'gift.tea').w);
      o.again = giftGive(p, 'herbs'); o.carry = P.carry.slice();
      const q = SOC.crew.find(x => x !== p && !giftTaste(x).loves.includes('made') && !giftTaste(x).likes.includes('made')); P.carry = ['keyring']; const b = giftGive(q, 'keyring'); o.polite = b && b.how;
      o.known = relGet(p.id).known.some(k => /^Loves /.test(k));
      o.keep = [giftKeepsake(p, 'a test keepsake'), giftKeepsake(p), keepsakes().length, !!mem(p.id, 'keepsake')];
      // a crew gift: make Tomas a warm friend, run a few evenings
      relAdd('tomas', 'chat', 70); memAdd('tomas', 'moment.test'); SHIP.social.given = []; const m0 = SHIP.social.mail.length;
      for (let h = SHIP.social.hour - SHIP.social.hour % 24 + 19, k = 0; k < 28; k++, h += 24) socCrewGift(h);
      o.given = SHIP.social.given.length; o.mail = SHIP.social.mail.length - m0;
      const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); o.saved = s === JSON.stringify(socSave());
      P.carry = carry; SHIP.social.given = []; SHIP.social.keepsakes = []; SHIP.social.mail.length = m0; SHIP.mem = {};
      o.who = p.id; o.taste = t; return o;
    })()""")
    print('Gifts:', json.dumps(gf))
    if gf['add'] != [True, False, True, False] or gf['hands'] != 'tin of tea': fail('giftAdd / giftInHands wrong')
    if gf['first'] != 'loved' or gf['pts'] < 10 or gf['mem'] != 90 or gf['again'] is not None or gf['carry'] != ['herbs']: fail('a loved gift lands wrong, or a second gift the same week went through')
    if gf['polite'] != 'polite' or not gf['known']: fail('a polite gift, or "Loves ..." in what you know, wrong')
    if gf['keep'] != [True, False, 1, True]: fail(f"keepsakes wrong: {gf['keep']}")
    if not (1 <= gf['given'] <= 4) or gf['mail'] != gf['given'] or not gf['saved']: fail(f"crew gifts wrong: {gf['given']} in 4 weeks, mail {gf['mail']}")

    # 10. reputation (0.36.25): sources, floors and recovery, bands and their consequences, the weekly pass
    rq = g.ev(r"""(() => {
      const o = {}, keepRel = JSON.stringify(socSave()); SHIP.rep = null;
      o.start = repView().depts.filter(x => x.band !== 'new').map(x => x.dept);
      const oven = machineList().find(x => x.kind === 'oven'); o.ovenDept = repDeptOf(oven);
      repNote('repair', { who: 'you', machine: oven.id }); o.afterFix = SHIP.rep.dept[o.ovenDept];
      repNote('repair', { who: 'pell', machine: oven.id }); o.notMine = SHIP.rep.dept[o.ovenDept];
      for (let i = 0; i < 12; i++) repNote('jobAbandoned', { machine: oven.id }); o.floor0 = SHIP.rep.dept[o.ovenDept];
      const g1 = SOC.crew.find(p => p.dept === o.ovenDept); relGet(g1.id).pts = 100; relGet(g1.id).tier = 4;
      repNote('jobAbandoned', { machine: oven.id }); o.floorFriend = [repFloor(o.ovenDept), SHIP.rep.dept[o.ovenDept]];
      SHIP.rep.dept[o.ovenDept] = 2; repWeek(6 * 24 + 4); o.recover = SHIP.rep.dept[o.ovenDept];
      for (let i = 0; i < 12; i++) repNote('repair', { who: 'you', machine: oven.id, state: 'failing' });
      o.band = repBand(o.ovenDept); o.asked = repAskedFor(o.ovenDept);
      const fresh = SOC.crew.find(p => p.dept === o.ovenDept && !SHIP.rel[p.id]); o.warmStart = fresh ? relGet(fresh.id).pts : null;
      o.knownFor = knownFor();
      o.mail = SHIP.social.mail.some(m => m.subject === 'From all of us');
      repNote('shiftStart', { late: 40 }); repNote('shiftStart', { late: 35 }); const w0 = SHIP.rep.ship.work; repWeek(13 * 24 + 4);
      o.pull = [w0, SHIP.rep.ship.work]; o.calder = repNotes().map(n => n.text);
      o.view = repView();
      const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); o.saved = s === JSON.stringify(socSave());
      socLoad(JSON.parse(keepRel)); return o;
    })()""")
    print('Reputation:', json.dumps(rq))
    if rq['start'] != []: fail(f"nobody should know you at the start: {rq['start']}")
    if rq['ovenDept'] != 'galley' or rq['afterFix'] != 13 or rq['notMine'] != 13 or rq['floor0'] != 0: fail('repairs and dips wrong')
    if rq['floorFriend'] != [5, 5] or rq['recover'] != 3: fail(f"floors and recovery wrong: {rq['floorFriend']} {rq['recover']}")
    if rq['band'] not in ('well', 'theirs') or not rq['asked'] or rq['warmStart'] != 8: fail('bands and their consequences wrong')
    if 'reliable' not in rq['knownFor'] or not rq['calder'] or not any('late' in t for t in rq['calder']): fail('known for, or Calder\'s note, wrong')
    if not rq['saved'] or any(c.isdigit() for c in json.dumps(rq['view']['ship'])): fail('the reputation view shows numbers, or the save differs')

    # 11. invitations (0.36.26): at most two a day, to traditions and from friends, each fitting the person's real plan
    iv = g.ev(r"""(() => {
      const o = { days: [], bad: [] }, keepS = JSON.stringify(socSave()), keepA = SHIP.device.appts.slice(), t0 = shipNow(); SHIP.device.appts.length = 0;
      for (const id of ['tomas', 'pell', 'rina']) { relGet(id).pts = 70; relGet(id).tier = 3; }
      for (const p of SOC.crew.slice(0, 25)) if (!SHIP.rel[p.id]) { relGet(p.id).pts = 35; relGet(p.id).tier = 2; }
      SHIP.social.invites = [];
      for (let d = 2; d <= 15; d++) {
        setShipNow((d - 1) * 1440 + 420); socInvites((d - 1) * 24 + 7);
        const today = SHIP.social.invites.filter(x => x.day === d); o.days.push(today.length);
        for (const x of today) {
          const a = SHIP.device.appts.find(y => y.id === x.appt), p = SOC.crew[SOC.idx.get(x.from)];
          const fits = a && planDay(p, d).some(s => s.placeId === a.where && s.from <= a.at && s.to >= a.at + Math.min(a.len, 15));
          if (!fits) o.bad.push([d, x.from, x.kind, x.trad]);
        }
        if (d === 9) { const x = today[0]; if (x) { o.line = chatLine(SOC.crew[SOC.idx.get(x.from)], shipNow()); setShipNow((d - 1) * 1440 + 905); const m0 = (SHIP.mail || []).length; socInviteMail(shipNow()); o.mail = (SHIP.mail || []).length - m0; } }
      }
      o.kinds = {}; for (const x of SHIP.social.invites) o.kinds[x.kind] = (o.kinds[x.kind] || 0) + 1;
      SHIP.device.appts.length = 0; SHIP.device.appts.push(...keepA); setShipNow(t0); socLoad(JSON.parse(keepS));
      return o;
    })()""")
    print('Invitations:', json.dumps(iv))
    if max(iv['days']) > 2 or sum(iv['days']) < 4 or iv['bad']: fail(f"invitations wrong: per day {iv['days']}, not fitting their plan {iv['bad']}")
    if iv.get('line') and iv['line']['kind'] != 'invite': fail(f"the inviter's tap line should be the invitation: {iv.get('line')}")

    # 12. bunk visits and notes (0.36.27): a friend knocks in the evening when you're in your bunk room; notes when you're out
    vs = g.ev(r"""(() => {
      const o = { visits: [], notes: [] }, keepS = JSON.stringify(socSave()), t0 = shipNow();
      for (const id of ['tomas', 'pell', 'rina']) { relGet(id).pts = 70; relGet(id).tier = 3; }
      o.home = playerInBunk();
      for (let d = 8; d <= 17 && o.visits.length < 3; d++) for (let m = 1100; m < 1340; m++) {
        setShipNow((d - 1) * 1440 + m); socialVisit((d - 1) * 1440 + m);
        if (VISIT && !VISIT.inside) { o.visits.push([d, m, VISIT.p.id]); if (o.visits.length === 1) { const realCome = typeof crewComeTo === 'function' ? crewComeTo : undefined; crewComeTo = (p, id, cb) => { cb(); return () => {}; };   // section 10's walk-in, arriving at once
          visitIn(); crewComeTo = realCome; o.card = CHAT && [CHAT.line.kind, CHAT.visit, !!mem(VISIT.p.id, 'visit')]; } else { VISIT.until = 0; socialVisit(0); } }
        if (m === 1325 && o.visits.length === 1 && o.closed === undefined) o.closed = VISIT === null;
        if (m === 1325) chatClose();
        if (m > 1290 && VISIT && !VISIT.inside) o.late = true;
      }
      chatClose(); seekEnd(); VISIT = null; SHIP.social.notes = []; const P0 = player.obj.position.clone(); player.obj.position.copy(cellPos(...deckDef.lift)); o.out = !playerInBunk();
      for (let d = 20; d <= 34 && o.notes.length < 2; d++) for (let m = 1140; m < 1290; m++) { setShipNow((d - 1) * 1440 + m); socialVisit((d - 1) * 1440 + m); const n = SHIP.social.notes.length; if (n > o.notes.length) o.notes.push([d, m]); }
      o.read = [bunkNote(), bunkNote()]; o.read[1] = o.read[1] && o.read[1].text;
      o.days = new Set(o.visits.map(v => v[0])).size === o.visits.length;
      const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); o.saved = s === JSON.stringify(socSave());
      player.obj.position.copy(P0); setShipNow(t0); socLoad(JSON.parse(keepS)); return o;
    })()""")
    print('Visits:', json.dumps(vs))
    if len(vs['visits']) < 2 or not vs['days'] or vs.get('late') or vs.get('card', [None])[:2] != ['visit', True] or not vs['card'][2]: fail('bunk visits wrong')
    if vs.get('closed') is not True: fail('a visitor should leave at 22:00')
    if not vs.get('out') or not vs['notes'] or not vs['read'][0] or not vs['saved']: fail('notes on your bunk wrong')

    # 13. crew come and go (0.36.28): a transfer's news, the goodbye, the day, letters after; an arrival's news, new for a week
    cg = g.ev(r"""(() => {
      const o = {}, keepS = JSON.stringify(socSave()), t0 = shipNow(), pell = SOC.crew[SOC.idx.get('pell')], x = SOC.crew.find(p => !p.story && p.dept === 'survey');
      pell.aboard = [null, 20]; x.aboard = [15, null];
      setShipNow(6 * 1440); socReset(6 * 24); relGet('pell').pts = 70; relGet('pell').tier = 3; relGet('pell').met = 6 * 1440; memAdd('pell', 'fav.lamp');
      const step = (d0, d1) => { for (let d = d0; d <= d1; d++) { setShipNow((d - 1) * 1440 + 480); socialTo(shipNow()); } };
      step(7, 10); o.news = NEWS.some(n => n.id === 'leaving:pell') && NEWS.some(n => n.id === 'arriving:' + x.id);
      o.before = crewContacts({ all: true }).some(c => c.id === x.id);
      step(11, 18); o.bye = chatLine(pell, shipNow()).kind; o.byeText = chatLine(pell, shipNow()).text;
      const m0 = SHIP.social.mail.length; step(19, 21); o.moved = movedOn().map(m => m.id); o.sorry = SHIP.social.mail.slice(m0).some(m => /missed you/.test(m.subject));
      o.gone = !crewContacts({ all: true }).some(c => c.id === 'pell') && movedOff('pell') && !movedOff('tomas') && newHere(x.id, 16); o.newHere = [newHere(x, 16), newHere(x, 23)];
      const m1 = SHIP.social.mail.length; step(22, 50); o.letters = SHIP.social.mail.slice(m1).filter(m => m.from.startsWith(pell.name)).length;
      const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); o.saved = s === JSON.stringify(socSave());
      delete pell.aboard; delete x.aboard; setShipNow(t0); socLoad(JSON.parse(keepS)); return o;
    })()""")
    print('Coming and going:', json.dumps(cg))
    if not cg['news'] or cg['before'] or cg['bye'] != 'goodbye' or cg['moved'] != ['pell'] or not cg['gone']: fail('transfers wrong (news, goodbye, moved on)')
    if not cg['sorry'] or cg['newHere'] != [True, False] or not (2 <= cg['letters'] <= 4) or not cg['saved']: fail('the day, new arrivals or letters wrong')

    # 14. section 21's asked-for waves (0.36.58): socialSeekAsk windows, once each, saved; a 'favour' why makes their favour come that day
    sk = g.ev(r"""(() => { const keep = JSON.stringify(socSave()), t = Math.floor(shipNow());
      const ok = [socialSeekAsk('tomas', { from: t + 10, until: t + 100, why: 'intro:tomas' }), socialSeekAsk('nobody', { from: t, until: t + 10 })];
      const win = [!!seekAskFor('tomas', t), !!seekAskFor('tomas', t + 50), !!seekAskFor('tomas', t + 100)];
      const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); const saved = !!seekAskFor('tomas', t + 50);
      const p = SOC.crew.find(q => q.work && q.work.place && !STORY_ARCS[q.id] && !SHIP.rel[q.id]);
      let fav = null; if (p && typeof favourPost === 'function') { socialSeekAsk(p.id, { from: t, until: t + 90, why: 'intro:d4-favour' }); fav = !!favourOf(p); }
      socLoad(JSON.parse(keep)); return { ok, win, saved, fav }; })()""")
    print('Asked-for waves:', sk)
    walk = g.ev(r"""(() => { const keep = JSON.stringify(socSave()), t0 = shipNow(), tomas = SOC.crew[SOC.idx.get('tomas')];
      let t = null; for (let k = 0; k < 7 * 1440 && t === null; k += 30) { const w = whereIs(tomas, t0 + k); if (w && !w.moving && (w.act === 'leisure' || w.act === 'off')) t = t0 + k; }
      if (t === null) return { skip: true };
      setShipNow(t); seekEnd(); chatClose(); SHIP.social.seekAsks = []; socialSeekAsk('tomas', { from: t - 5, until: t + 120, why: 'intro:tomas' });
      const real = typeof crewComeTo === 'function' ? crewComeTo : undefined; let walked = 0;
      crewComeTo = (p, id, cb) => { walked++; cb(); return () => {}; };   // section 10's walk, arriving at once
      const P0 = player.obj.position.clone(), lift = DECKS[deckDef.num].lift; player.obj.position.copy(cellPos(...lift));
      socialSeek(Math.floor(t)); const o = { walked, chip: !!(SEEK && SEEK.p === tomas), done: SHIP.social.seekAsks[0].done };
      socialSeek(Math.floor(t) + 1); o.once = walked === 1;
      crewComeTo = real; seekEnd(); player.obj.position.copy(P0); setShipNow(t0); socLoad(JSON.parse(keep)); return o; })()""")
    print('An asked-for wave walks to you:', walk)
    if not walk.get('skip') and (walk['walked'] != 1 or not walk['chip'] or not walk['done'] or not walk['once']): fail(f'the asked-for wave does not happen: {walk}')
    if sk['ok'] != [True, False] or sk['win'] != [False, True, False] or not sk['saved'] or sk['fav'] is False: fail(f'socialSeekAsk wrong: {sk}')

    # 15. a favour handed in on the card (0.36.62): the memory and the reputation it gives
    fv = g.ev(r"""(() => { if (typeof favourPost !== 'function') return null;
      const keep = JSON.stringify(socSave()), p = SOC.crew.find(q => !STORY_ARCS[q.id] && q.dept !== 'works');
      SHIP.mem = {}; SHIP.rep = null;
      const id = favourPost({ from: p.id, title: 'Test favour', kind: 'lamp', stops: [] }); favourAccept(id);
      chatClose(); CHAT = { p, line: { text: '', say: true }, ask: false, fav: null, at: shipNow(), reach: 99 };
      chatDo('help'); const o = { mem: !!mem(p.id, 'fav.lamp'), kind: SHIP.rep ? SHIP.rep.ship.kindness : null, dept: SHIP.rep ? SHIP.rep.dept[p.dept] : null };
      chatClose(); socLoad(JSON.parse(keep)); return o; })()""")
    print('A favour handed in:', fv)
    if fv is not None and (not fv['mem'] or not fv['kind'] or fv['kind'] <= 50): fail(f'handing in a favour gives no memory or reputation: {fv}')

    # 16. guiding a newcomer (0.36.65, A10): only once promoted; Calder assigns a new cadet a week ahead (card, else Mail),
    # it starts on their arrival day (onboarding's introGuide), their questions with three answers, settled a week on; hand back
    gd = g.ev(r"""(() => {
      const keep = JSON.stringify(socSave()), t0 = shipNow(), F = SHIP.flags || (SHIP.flags = {}), kf = { promoted: F.promoted, ga: F['guide.active'] };
      const x = SOC.crew.find(p => p.cadet), cal = SOC.crew[SOC.idx.get('calder')], ab = x && x.aboard, A = 43, o = {};
      if (!x || !cal) return { skip: true };
      const stub = typeof introGuide !== 'function', calls = []; if (stub) { window.introGuide = id => calls.push(['go', id]); window.introGuideEnd = id => calls.push(['end', id]); }
      const step = (d0, d1) => { for (let d = d0; d <= d1; d++) { setShipNow((d - 1) * 1440 + 480); socialTo(shipNow()); } };
      x.aboard = [A, null]; setShipNow(32 * 1440); socReset(32 * 24); repAdd('works', 40);
      step(34, 37); o.off = !SHIP.social.guide;                       // not promoted: nothing
      flagSet('promoted', true); setShipNow(32 * 1440); socReset(32 * 24); repAdd('works', 40);
      step(34, 36); const G = SHIP.social.guide; o.assigned = G ? [G.id === x.id, G.at, G.day] : null; o.ask = chatLine(cal, shipNow()).kind;
      step(37, 37); o.mail = SHIP.social.mail.some(m => m.subject === 'A newcomer for you') && G.told; o.notYet = !G.on;
      step(38, A); o.on = [G.on, !!flag('guide.active'), relTier(x.id), bondOf(x.id, 'mentor'), stub ? calls.some(c => c[0] === 'go' && c[1] === x.id) : true];
      socIntroNote({ step: 'hello', who: x.id }); o.stepMem = !!mem(x.id, 'guide.hello');
      const q = chatLine(x, shipNow()); o.q = [q.kind, (q.answers || []).length];
      chatClose(); CHAT = { p: x, line: q, ask: false, fav: null, at: shipNow(), reach: 99 }; let got = []; const dr = CHAT_SKIN.draw; CHAT_SKIN.draw = (el, v) => { got = v.buttons.map(b => b.label); }; chatShow();
      o.buttons = got.length;
      const k0 = repInit().ship.kindness; chatDo('nq:2'); o.answered = [G.qs, repInit().ship.kindness > k0, chatLine(x, shipNow()).kind !== 'newcomer'];
      CHAT = { p: cal, line: { text: '', say: true }, ask: false, fav: null, at: shipNow(), reach: 99 }; chatShow();
      o.handBtn = got.some(b => /^Hand /.test(b)); CHAT_SKIN.draw = dr; chatClose();
      const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); o.saved = s === JSON.stringify(socSave());
      step(A + 1, A + 8); const G2 = SHIP.social.guide; o.settled = [G2.end, !!flag('guide.active'), knownFor().includes('good with newcomers'), SHIP.social.mail.some(m => /settled in/.test(m.subject))];
      setShipNow(32 * 1440); socReset(32 * 24); repAdd('works', 40); step(34, A);   // hand back on Calder's card
      CHAT = { p: cal, line: { text: '', say: true }, ask: false, fav: null, at: shipNow(), reach: 99 }; chatDo('guide-back'); chatClose();
      o.back = [SHIP.social.guide && SHIP.social.guide.end, !!flag('guide.active'), bondOf(x.id, 'mentor') === 'you', stub ? calls.some(c => c[0] === 'end') : true];
      if (stub) { delete window.introGuide; delete window.introGuideEnd; }
      x.aboard = ab; if (kf.promoted === undefined) delete F.promoted; else F.promoted = kf.promoted; if (kf.ga === undefined) delete F['guide.active']; else F['guide.active'] = kf.ga;
      setShipNow(t0); socLoad(JSON.parse(keep)); return o; })()""")
    print('Guiding a newcomer:', json.dumps(gd))
    if not gd.get('skip'):
        if not gd['off'] or not gd['assigned'] or gd['assigned'] != [True, 36, 43] or gd['ask'] != 'guide' or not gd['mail'] or not gd['notYet']: fail(f'the newcomer assignment wrong: {gd}')
        if gd['on'] != [True, True, 1, 'you', True] or not gd['stepMem'] or gd['q'] != ['newcomer', 3] or gd['buttons'] != 3: fail(f'guiding a newcomer does not start right: {gd}')
        if gd['answered'] != [1, True, True] or not gd['handBtn'] or not gd['saved'] or gd['settled'] != ['settled', False, True, True] or gd['back'] != ['handed', False, False, True]: fail(f'guiding a newcomer wrong: {gd}')

    # 17. your own room (0.36.66, A11): Come over on a friend's card once promoted, an appointment at your quarters, the host line when kept
    hs = g.ev(r"""(() => {
      const keep = JSON.stringify(socSave()), t0 = shipNow(), F = SHIP.flags || (SHIP.flags = {}), kp = F.promoted, D = SHIP.device;
      if (!D || !Array.isArray(D.appts) || typeof playerBed !== 'function') return { skip: true };
      const n0 = D.appts.length, o = {}, dr = CHAT_SKIN.draw; let got = []; CHAT_SKIN.draw = (el, v) => { got = v.buttons.map(b => b.label); };
      setShipNow(9 * 1440 + 720); const tomas = SOC.crew[SOC.idx.get('tomas')], r = relGet('tomas'); r.pts = 70; r.tier = 3; r.hostDay = 0;
      const card = () => { chatClose(); CHAT = { p: tomas, line: { text: '', say: true }, ask: false, fav: null, at: shipNow(), reach: 99 }; chatShow(); return got.slice(); };
      o.off = !card().includes('Come over');
      flagSet('promoted', true); o.on = card().includes('Come over');
      chatDo('host'); o.said = CHAT && CHAT.line.text; o.again = card().includes('Asked over');
      const a = D.appts.slice(n0).find(x => x.host), bed = playerBed(), L = DECKS[deckOf(bed)].places, room = L.find(q => q.id === bed).room;
      o.appt = a ? [a.status, a.with[0], L.find(q => q.id === a.where).room === room, a.where !== bed || !L.some(q => q.room === room && q.id !== bed), a.at % 1440 >= 1170] : null;
      if (a) { const k0 = repInit().ship.kindness; a.status = 'kept'; chatClose(); socialAppts(); o.kept = [!!mem('tomas', 'hosted'), CHAT && CHAT.line.kind, repInit().ship.kindness > k0, !!CHAT && CHAT.visit]; }
      const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); o.saved = SHIP.rel.tomas.hostDay === 10;
      chatClose(); VISIT = null; CHAT_SKIN.draw = dr; D.appts.length = n0; if (kp === undefined) delete F.promoted; else F.promoted = kp;
      setShipNow(t0); socLoad(JSON.parse(keep)); return o; })()""")
    print('Your own room:', json.dumps(hs))
    if not hs.get('skip'):
        if not hs['off'] or not hs['on'] or not hs['again'] or not hs['saved']: fail(f'Come over button wrong: {hs}')
        if hs['appt'] and (hs['appt'][:2] != ['yes', 'tomas'] or not all(hs['appt'][2:]) or hs.get('kept') != [True, 'host', True, True]): fail(f'Come over appointment or visit wrong: {hs}')
        if not hs['appt'] and 'Not tonight' not in (hs['said'] or ''): fail(f'Come over made no appointment: {hs}')

    # 18. small seams (0.36.68): the roster's short theme fields through socialFill ("" is none); the hour of the day on Day 0; one unclaimed-job dip a department a week (0.36.71)
    sm = g.ev(r"""(() => { const p = { ...SOC.crew[SOC.idx.get('tomas')], kin: 'my gran', lost: '', hobbyNoun: ' chess ' };
      const keep = JSON.stringify(socSave()), t0 = shipNow(); SHIP.rep = null; const g0 = repInit().dept.galley;   // unclaimed jobs: one dip a department a week (0.36.71)
      setShipNow(7 * 1440 + 600); repNote('jobUnclaimed', { dept: 'galley' }); setShipNow(9 * 1440 + 600); repNote('jobUnclaimed', { dept: 'galley' }); const g1 = repInit().dept.galley;
      setShipNow(15 * 1440 + 600); repNote('jobUnclaimed', { dept: 'galley' }); const g2 = repInit().dept.galley; setShipNow(t0); socLoad(JSON.parse(keep));
      const q = seekSpot(), kp = PLAYER_PLACE; let mine = true; if (q) { PLAYER_PLACE = q.id; const q2 = seekSpot(); mine = !q2 || q2.id !== q.id; PLAYER_PLACE = kp; }   // never your own seat (0.36.72)
      const D = SHIP.device, n0 = D && D.appts ? D.appts.length : 0; let occ = true;   // occasions' appointments (section 19's apptAdd, a.occ): no points, no remark (0.36.74)
      if (D && D.appts) { const r0 = relGet('holt').pts; D.appts.push({ id: 9901, with: ['holt'], at: shipNow() - 60, len: 30, where: 'x', kind: 'summons', status: 'kept', occ: 'readyroom' }, { id: 9902, with: ['holt'], at: shipNow() - 30, len: 30, where: 'x', kind: 'summons', status: 'missed', occ: 'readyroom' });
        socialAppts(); occ = relGet('holt').pts === r0 && !apptMissedBy(SOC.crew[SOC.idx.get('holt')]); D.appts.length = n0; }
      return [socialFill(p, 'kin'), socialFill(p, 'lost'), socialFill(p, 'hobbyNoun'), socHr(-5), socHr(31), g0 - g1, g0 - g2, socDuration(600), socDuration(650), mine, occ]; })()""")
    print('Small seams:', sm)
    if sm != ['my gran', None, 'chess', 19, 7, 1, 2, 'twenty months', 'nearly two years', True, True]: fail(f'kin / lost / hobbyNoun, socHr or the weekly unclaimed dip wrong: {sm}')

    print('errors', g.errors[:5])
    if g.errors: ok = False
    print('SOCIAL CHECK OK' if ok else 'SOCIAL CHECK FAILED')
    g.close()
