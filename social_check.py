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
    sample: NEWS.slice(-6).map(x => x.lines[0]), mem: Object.fromEntries(Object.entries(SHIP.mem).map(([k, l]) => [k, l.map(m => m[0] + ' ' + Math.round(m[2]))])), rep: SHIP.rep && { dept: SHIP.rep.dept, ship: SHIP.rep.ship, view: repView() } };
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

    print('Memories after the run:', json.dumps(a['mem']))
    m = a['mem']
    if not any(x.startswith('chat ') for x in m.get('tomas', [])): fail('Tomas should remember chatting')
    if not any(x.startswith('moment.test.1 ') for x in m.get('rina', [])): fail("Rina's big memory should last two weeks")
    if any(x.startswith('missed.test') for x in m.get('pell', [])): fail("Pell's sour memory should have faded")
    if 'intro.arrival 100' not in m.get('pell', []): fail('a core memory should stay at 100')
    if not any(k != 'rina' and any(x.startswith('heard.moment.test.1') for x in l) for k, l in m.items()): print('  (nobody heard of the big memory: Rina has no friends at 40+)')

    rp = a['rep']
    print('Reputation after the run:', json.dumps(rp and {'dept': rp['dept'], 'ship': rp['ship'], 'knownFor': rp['view']['knownFor']}))
    if not rp or rp['dept']['galley'] < 20 or max(v for k, v in rp['dept'].items() if k not in ('galley', 'works')) >= 20: fail('a stand-in who fixes galley ovens should be known in the galley, and only there')

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
      for (const id of ['tomas', 'pell', 'rina']) relAdd(id, 'chat', 30);
      const all = () => JSON.stringify(crew.flatMap(p => [0, 1, 2, 3, 4, 5].map(k => chatLine(p, t0 + 60 * k))));
      const base = all(); window.lineFor = () => null; o.nullSame = all() === base;
      const asked = {}; window.lineFor = (p, kind, ctx) => { asked[kind] = (asked[kind] || 0) + 1; return { text: kind + ':' + p.id, id: kind, kind }; };
      memAdd('tomas', 'fav.lamp'); socNote('repair', { who: 'you', kind: 'oven' });
      const kinds = {}; for (const p of SOC.crew) for (let k = 0; k < 6; k++) { const l = chatLine(p, t0 + 60 * k); kinds[l.kind] = (kinds[l.kind] || 0) + 1; }
      o.kinds = kinds; o.asked = asked;
      o.tomas = [0, 1, 2, 3, 4, 5, 6, 7].map(k => chatLine(SOC.crew[SOC.idx.get('tomas')], t0 + 60 * k).kind);
      delete window.lineFor; o.back = all() === base;
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
      SHIP.intro = { step: 'arrival', escort: 'torres-zeke' }; window.flag = k => F.has(k);
      o.shut = ['d2', 'd3', 'd5', 'done'].map(socGate); F.add('week1.d2'); F.add('week1.d3'); o.tue = ['d2', 'd3', 'd5', 'done'].map(socGate);
      introNote({ step: 'arrival', who: ['torres-zeke'] }); introNote({ step: 'dinner', who: [] }); introNote({ step: 'look', who: ['pell'] });
      o.mem = [mem('torres-zeke', 'intro.arrival') && mem('torres-zeke', 'intro.arrival').w, !!mem('calder', 'intro.dinner'), !!mem('pell', 'intro')];
      o.mentor = [SHIP.social.mentor, bondOf('torres-zeke', 'mentee'), socialFill(SOC.crew[SOC.idx.get('torres-zeke')], 'mentee')];
      window.lineFor = (p, kind) => kind === 'week1' ? { text: 'w1', id: 'w1', kind } : null;
      o.week1 = chatLine(SOC.crew[SOC.idx.get('torres-zeke')]).kind;
      F.add('week1.done'); o.done = [introOn(), socGate('done'), chatLine(SOC.crew[SOC.idx.get('torres-zeke')]).kind !== 'week1'];
      delete window.lineFor; SHIP.intro = null; if (had) window.flag = had; else delete window.flag;
      const s = JSON.stringify(socSave()); socLoad(JSON.parse(s)); o.saved = SHIP.social.mentor === 'torres-zeke';
      SHIP.social.mentor = null; SHIP.mem = {};
      // an invitation to a tradition someone is going to
      let hit = null;
      for (let d = 2; d <= 14 && !hit; d++) for (const e of eventsOn(d)) { if (hit) break; for (const p of SOC.crew) { const seg = planDay(p, d).find(x => x.placeId && x.tag && x.tag.startsWith('ev-' + e.id)); if (seg) { hit = { d, id: e.id, p: p.id, seg }; break; } } }
      if (hit) {
        const keep = SHIP.device.appts.slice(), t = shipNow(); setShipNow((hit.d - 1) * 1440 + 360);
        const id = socialInvite({ trad: hit.id, day: hit.d, from: hit.p }), a = SHIP.device.appts.find(x => x.id === id);
        o.invite = { trad: hit.id, day: hit.d, ok: !!a && a.status === 'asked' && a.kind === 'invite' && a.by === hit.p && a.where === hit.seg.placeId && a.at === (hit.d - 1) * 1440 + hit.seg.from,
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
      const p = SOC.crew.find(q => giftTaste(q).loves.includes('tea')) || SOC.crew[0], t = giftTaste(p);
      const pts0 = relGet(p.id).pts; P.carry = []; o.add = [giftAdd('tin of tea'), giftAdd('a spanner'), giftAdd('herbs'), giftAdd('biscuits')];
      o.hands = giftInHands();
      const a = giftGive(p, 'tin of tea'); o.first = a && a.how; o.pts = Math.round((relGet(p.id).pts - pts0) * 100) / 100; o.mem = mem(p.id, 'gift.tea') && Math.round(mem(p.id, 'gift.tea').w);
      o.again = giftGive(p, 'herbs'); o.carry = P.carry.slice();
      const q = SOC.crew.find(x => x !== p && !giftTaste(x).loves.includes('made') && !giftTaste(x).likes.includes('made')); P.carry = ['keyring']; const b = giftGive(q, 'keyring'); o.polite = b && b.how;
      o.known = relGet(p.id).known.some(k => /^Loves /.test(k));
      o.keep = [giftKeepsake(p, 'a test keepsake'), giftKeepsake(p), keepsakes().length, !!mem(p.id, 'keepsake')];
      // a crew gift: make Tomas a warm friend, run a few evenings
      relAdd('tomas', 'chat', 70); memAdd('tomas', 'chat'); SHIP.social.given = []; const m0 = SHIP.social.mail.length;
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
    if rq['start'] != ['works']: fail(f"only Works should know you at the start: {rq['start']}")
    if rq['ovenDept'] != 'galley' or rq['afterFix'] != 13 or rq['notMine'] != 13 or rq['floor0'] != 0: fail('repairs and dips wrong')
    if rq['floorFriend'] != [5, 5] or rq['recover'] != 3: fail(f"floors and recovery wrong: {rq['floorFriend']} {rq['recover']}")
    if rq['band'] not in ('well', 'theirs') or not rq['asked'] or rq['warmStart'] != 8: fail('bands and their consequences wrong')
    if 'reliable' not in rq['knownFor'] or not rq['calder'] or not any('late' in t for t in rq['calder']): fail('known for, or Calder\'s note, wrong')
    if not rq['saved'] or any(c.isdigit() for c in json.dumps(rq['view']['ship'])): fail('the reputation view shows numbers, or the save differs')

    print('errors', g.errors[:5])
    if g.errors: ok = False
    print('SOCIAL CHECK OK' if ok else 'SOCIAL CHECK FAILED')
    g.close()
