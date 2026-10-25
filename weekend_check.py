# Starship Cadet: the weekend traditions check (0.92.5 item 16; FX14's T1-T2, FX11's T3-T4 on; keep in the repo)
# Runs on a copy of the build with WEEKEND_ON on (on in the game from 0.92.5; older builds had a URL flag), and a copy with it off as the base:
#   every weekend tradition on its day (eventsOn), and nothing of them with the switch off
#   each join has its activity (PLAYER_ACTS['tj:<id>'], made after the slot adds the joins: tjActs) and a join ends
#   Bread day (T3): crew at the kneading spots (Cook-along's 3-cookalong-*), the island's flour and tins (breadDay), you knead, and your
#     loaf is in Monday's breakfast basket (loafCard) 06:30-10:00 and not on Tuesday
#   The big jigsaw (T4): crew at the observation room's table, the puzzle on it (bigJigsaw) only on its Sunday afternoon
#     (Deck 1 as before on other days), a turn is 20 minutes and counts as your puzzles hobby
#   RV14's seat line: each weekend join you sit for puts you in a seat, sitting (tradSpot's seat-first), not standing
#   T5 (FX16): the deck head counts at each (a table), the picnic's basket and the cocoa pot only while they're on
#   no page errors
# Setup and environment as for cadet_test.py.  Run:  python3 weekend_check.py BUILD.html
import sys, json, re
exec(open(__file__.replace('weekend_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

ok = True
def check(cond, msg):
    global ok
    print(('ok   ' if cond else 'FAIL ') + msg)
    if not cond: ok = False
    return cond

build = sys.argv[1]; src = pathlib.Path(build).read_text()
# (FX16) on in the game from 0.92.5: the shipped build is the switch-on one, and a copy with it false is the base; a build from
# before the switch-on (a URL flag) is switched on in a copy, as before
SW = r"^const WEEKEND_ON = (?:URL_FLAGS\.has\('weekend'\)|true)"
check(bool(re.search(SW, src, flags=re.M)), 'the build has the WEEKEND_ON switch')
on = re.sub(SW, "const WEEKEND_ON = true", src, count=1, flags=re.M); off = re.sub(SW, "const WEEKEND_ON = false", src, count=1, flags=re.M)
won = str(WORK / 'test' / ('_weekend_' + pathlib.Path(build).name)); pathlib.Path(won).write_text(on)
build = str(WORK / 'test' / ('_weekend_off_' + pathlib.Path(build).name)); pathlib.Path(build).write_text(off)   # the base: the same build, the switch off
TRADS = {'saturday-run': 6, 'bread-day': 7, 'every-song': 69, 'gerald-clinic': 14, 'garden-picnic': 20, 'big-jigsaw': 21, 'night-owls-cocoa': 27, 'sunday-story': 28}   # a day each is on (the 4-week rotation, the user 2026-10-25: two a weekend; Every song's first is Day 69: Day 13 is the storm's lantern supper, and on Day 41 it gives way to a birthday)
DAYS = sorted(set(TRADS.values()))
EVS = "JSON.stringify(%s.map(d => [d, eventsOn(d).map(e => e.id)]))" % json.dumps(DAYS)
# (DS1, the user 2026-10-25: "spread the new ones across weeks, and keep some that were already there") every Saturday and
# Sunday of Days 6-84: the traditions that were already there, with their times, and the new ones on it
WKND = """JSON.stringify((() => { const out = []; for (let d = 6; d <= 84; d++) { if (weekday(d) < 5) continue;
  const L = eventsOn(d); out.push([d, weekday(d), L.filter(e => !WEEKEND_TRADS.has(e.id)).map(e => e.id + ' ' + e.from + '-' + e.to).sort(), L.filter(e => WEEKEND_TRADS.has(e.id)).map(e => e.id)]); } return out; })())"""
# lead 35's rule (RV14's rv14-old_trads.py folded in): with the switch on, every tradition that was already there keeps its days,
# times, places and host (Days 1-56, the switch off as the base: the same build), loses at most 2 people on any day, and never
# goes below its fewest on any day with the switch off (the format has no attendance minimum: its own worst day is the floor)
OLDT = """JSON.stringify((() => { const out = {}; for (let d = 1; d <= 56; d++) out[d] = eventsOn(d).filter(e => !WEEKEND_TRADS.has(e.id)).map(e => {
  const came = schedPeople().filter(p => planDay(p, d).some(s => evTagId(s.tag) === e.id)).map(p => p.id).sort();
  return [e.id, e.from, e.to, JSON.stringify(e.ev.where || null), e.ev.host || null, came]; }); return out; })())"""
# RV14: each weekend tradition's host planned at it, and how many go to each showing of the late ones
HOSTS = """JSON.stringify((() => { const out = []; for (let d = 6; d <= 84; d++) for (const e of eventsOn(d)) { if (!WEEKEND_TRADS.has(e.id)) continue;
  const goers = schedPeople().filter(p => planDay(p, d).some(s => evTagId(s.tag) === e.id)).map(p => p.id);
  const h = e.ev.host && ROSTER.find(p => p.id === e.ev.host), B = (d - 1) * 1440, pl = id => { const n = +String(id).split('-')[0]; return ((DECKS[n] || {}).places || []).find(q => q.id === id); }, room = h && planDay(h, d).some(s => s.placeId && s.from < B + e.to && s.to > B + e.from && pl(s.placeId) && [...(e.rooms || (e.rooms = eventRooms(e.ev)))].includes(s.placeId.split('-')[0] + '|' + pl(s.placeId).room));
  out.push([e.id, d, e.ev.host || null, !!e.ev.host && (goers.includes(e.ev.host) || !!room), goers.length]); } return out; })())"""   # (at it, or at work in its room through it: Brennan cooks in the galley on Bread day)

# T5 (FX16, the user's "deck head counts"): at the middle of each weekend tradition, Days 6-84, where everyone is planned to be,
# by deck (from the planner: the slot covering that minute and its deck; Deck 7 is the rec deck, R); printed as a table, the deck of the
# tradition marked; the last column is everyone else: away (guests and crew not aboard that day: the planner's 'away') or in the lift
HEADS = """JSON.stringify((() => { const out = []; for (let d = 6; d <= 84; d++) for (const e of eventsOn(d)) { if (!WEEKEND_TRADS.has(e.id)) continue;
  const B = (d - 1) * 1440, mid = B + Math.round((e.from + e.to) / 2), n = {}; let none = 0;
  for (const p of schedPeople()) { const s = planDay(p, d).find(x => x.from <= mid && x.to > mid); if (s && s.act !== 'away' && s.type !== 'lift' && s.deck) { const k = String(s.deck); n[k] = (n[k] || 0) + 1; } else none++; }
  out.push([e.id, d, (e.ev.where || [])[0] ? (e.ev.where[0].deck) : null, n, none]); } return out; })())"""

# T6 (FX16; FX12's rule, the user: birthdays at least an hour from any tradition): every birthday of a year, and the eight new ones
# near it (they give way: evBdaySlot drops one within the gap)
BDAY = """JSON.stringify((() => { const near = [], wk = []; let n = 0;
  for (let d = 1; d <= 364; d++) { const L = eventsOn(d), b = L.find(e => e.id === 'birthday'); if (!b) continue; n++;
    for (const e of L) if (WEEKEND_TRADS.has(e.id) && e.from < b.to + EV_BDAY.gap && b.from - EV_BDAY.gap < e.to) near.push([d, e.id, b.from, b.to, e.from, e.to]);
    if (weekday(d) >= 5) wk.push([d, b.from, L.filter(e => WEEKEND_TRADS.has(e.id)).map(e => e.id)]); }
  return { n, near, wk, gap: EV_BDAY.gap }; })())"""

with sync_playwright() as pw:
    g = Game(pw, build, 900, 760)
    evs = dict(json.loads(g.ev(EVS)))
    check(not any(i in evs[d] for i, d in TRADS.items()), 'switch off: none of the weekend traditions')
    off_w = json.loads(g.ev(WKND)); off_t = json.loads(g.ev(OLDT))
    g.close()
    g = Game(pw, won, 900, 760)
    evs = dict(json.loads(g.ev(EVS)))
    for i, d in TRADS.items(): check(i in evs[d], 'switch on: %s on Day %d' % (i, d))
    acts = json.loads(g.ev("JSON.stringify(Object.keys(TRAD_JOIN).filter(id => WEEKEND_TRADS.has(id) && !TRAD_JOIN[id].act).map(id => [id, !!PLAYER_ACTS['tj:' + id] && typeof PLAYER_ACTS['tj:' + id].until === 'function']))"))
    check(len(acts) >= 7 and all(a for _, a in acts), 'every weekend join has its activity, with an end (%s)' % acts)
    miss = json.loads(g.ev("JSON.stringify([...WEEKEND_TRADS].filter(id => !TRAD_JOIN[id] || (!TRAD_JOIN[id].act && !PLAYER_ACTS['tj:' + id])))"))
    check(not miss, 'every weekend tradition has a join, and each tap-join its activity (missing: %s)' % miss)
    SEATED = set(json.loads(g.ev("JSON.stringify([...WEEKEND_TRADS].filter(id => TRAD_JOIN[id] && /^sit/.test(TRAD_JOIN[id].pose || '')))")))
    print('  the weekend joins you sit for:', sorted(SEATED))
    on_w = json.loads(g.ev(WKND)); on_t = json.loads(g.ev(OLDT))
    floor = {}
    for d, L in off_t.items():
        for x in L: floor[x[0]] = min(floor.get(x[0], 99), len(x[5]))
    diff, lost3, under, shifts = [], [], [], 0
    for d in map(str, range(1, 57)):
        ea, eb = {x[0]: x for x in off_t[d]}, {x[0]: x for x in on_t[d]}
        for k in sorted(set(ea) | set(eb)):
            x, y = ea.get(k), eb.get(k)
            if not x or not y or x[:5] != y[:5]: diff.append((d, k, x and x[:5], y and y[:5])); continue
            lost = sorted(set(x[5]) - set(y[5]))
            if lost or set(y[5]) - set(x[5]): shifts += 1
            if len(lost) > 2: lost3.append((d, k, len(x[5]), len(y[5]), lost))
            if len(y[5]) < floor[k]: under.append((d, k, len(y[5]), floor[k]))
    print('  the old traditions with the switch on (Days 1-56): %d with a few people shifted; lost more than 2: %s; under their floor: %s' % (shifts, lost3[:4], under[:4]))
    check(not diff, 'lead 35: every old tradition keeps its days, times, places and host with the switch on (%s)' % diff[:3])
    check(not lost3 and not under, 'lead 35: no old tradition loses more than 2 people on a day, or goes below its fewest without the weekend ones (%s %s)' % (lost3[:3], under[:3]))
    moved = [(a[0], sorted(set(a[2]) ^ set(b[2]))) for a, b in zip(off_w, on_w) if a[2] != b[2]]
    print('  the weekends, Days 6-84 (day, new ones):', [(b[0], b[3]) for b in on_w])
    check(not moved, 'the rotation: every tradition that was already on a weekend is on the same days at the same times with the switch on (%s)' % moved[:4])
    ROT = [['saturday-run', 'bread-day'], ['every-song', 'gerald-clinic'], ['garden-picnic', 'big-jigsaw'], ['night-owls-cocoa', 'sunday-story']]   # lead 35's table
    want = {b[0]: ROT[((b[0] - 1) // 7) % 4][0 if b[1] == 5 else 1] for b in on_w}
    wrong = [(b[0], b[3]) for b in on_w if b[3] not in ([], [want[b[0]]])]
    gave = [(b[0], want[b[0]], 'storm day' if not b[2] else 'gave way') for b in on_w if not b[3]]
    print('  the rotation: none that day (the new one gave way to an old one, or a ship-wide event took the day):', gave)
    check(not wrong, 'the rotation: each weekend day has its own new one from the lead\'s table and no other (%s)' % wrong)
    check(all(any(b[3] == [i] for b in on_w) for i in TRADS) and len(gave) <= 6, 'the rotation: each of the eight on at least once in Days 6-84, and few giving way (%s)' % gave)
    hs = json.loads(g.ev(HOSTS))
    print('  hosts and goers (id, day, host, host there, going):', hs)
    check(all(h[3] for h in hs if h[2]), 'RV14: each weekend tradition\'s host is planned at it (%s)' % [h for h in hs if h[2] and not h[3]])
    bd = json.loads(g.ev(BDAY))
    print('  T6 birthdays on a weekend day with a new one due, Days 1-364 (day, birthday time, the new ones left that day):', bd['wk'])
    check(bd['n'] > 0 and not bd['near'], 'T6: no weekend tradition within %s minutes of a birthday, Days 1-364 (%d birthdays; near: %s)' % (bd['gap'], bd['n'], bd['near'][:4]))
    hd = json.loads(g.ev(HEADS)); decks = sorted({k for h in hd for k in h[3]}, key=lambda k: (not k.isdigit(), int(k) if k.isdigit() else 0, k))
    print('  T5 deck head counts at the middle of each (planned; * its deck; last: away or in the lift):')
    print('    %-17s %3s ' % ('tradition', 'day') + ' '.join('%5s' % ('R' if k == '7' else 'D' + k) for k in decks) + '  away')
    for h in hd: print('    %-17s %3d ' % (h[0], h[1]) + ' '.join('%5s' % ((('*' if str(h[2]) == k else '') + str(h[3].get(k, 0)))) for k in decks) + ' %5d' % h[4])
    late = [h for h in hs if h[0] in ('night-owls-cocoa', 'sunday-story')]
    check(late and all(h[4] >= 5 for h in late), 'RV14: at least 5 go to every Night owls\' cocoa and Sunday story (%s)' % late)
    g.close()
    # each tap-join on its day: starts, ends by itself in its tradition's time, and gives its own gain (RV13's ask)
    for jid, d in [(i, d) for i, d in TRADS.items() if i not in ('saturday-run',)]:
        g = Game(pw, won, 900, 760)
        r = json.loads(g.ev("""(() => { const d = %d, e = eventsOn(d).find(x => x.id === '%s'); if (!e) return JSON.stringify({ err: 'not on' });
          const w = (e.ev && e.ev.where || e.where || [])[0]; skipTo((d - 1) * 1440 + e.from + 6); goToDeck(w.deck, null); SHIP.device.settings.tips = false; return JSON.stringify({ to: e.to, deck: w.deck }); })()""" % (d, jid)))
        if 'err' in r: check(False, '%s: on Day %d' % (jid, d)); g.close(); continue
        g.step(200)
        st = json.loads(g.ev("""(() => { const e = eventsOn(%d).find(x => x.id === '%s'), s = TRAD_JOIN[e.id], need = s.need || 'social';
          const a = DECK_CREW.find(x => x.settled && x.spot && x.goalId && (evTagId(x.tag || '') === e.id || tradSpotIds({ ...e, day: %d }).has(x.spot.id))) || DECK_CREW.find(x => x.p.id === s.host);
          if (!a) return JSON.stringify({ err: 'nobody at it' }); SHIP.player.needs[need] = Math.min(SHIP.player.needs[need], 40);
          const rooms = e.rooms || (e.rooms = eventRooms(e.ev)), free = [...PLACE_OF.values()].filter(pl => rooms.has(deckDef.num + '|' + pl.room) && !heldBy(pl.id) && !BUSY.has(pl.id) && (placeSpot(pl.id) || {}).pose === 'sit').length;   // seats free in its rooms just before you join
          const n0 = SHIP.player.needs[need]; tradJoin({ ...e, day: %d }, a); const pl = ACT && ACT.placeId, sp = pl && placeSpot(pl);
          return JSON.stringify({ need, n0, act: ACT && ACT.kind, free, seat: [pl || null, sp ? sp.pose : null, ACT && ACT.o ? ACT.o.pose || null : null] }); })()""" % (d, jid, d, d)))
        if jid == 'sunday-story':   # RV14: a seated weekend join takes a seat first (tradSpot's seat-first, FX9's 7ff6a818), never the kettle (the common room has both; the bow lounge only seats)
            g.step(90); sp = json.loads(g.ev("(() => { const pl = ACT && ACT.placeId && ((DECKS[deckDef.num] || {}).places || []).find(q => q.id === ACT.placeId); return JSON.stringify([ACT && ACT.kind, ACT && ACT.placeId || null, pl ? pl.pose || null : null, player.pose || null]); })()"))
            check(str(sp[2] or '').startswith('sit') and 'kettle' not in str(sp[1]), '%s: your join puts you in a seat (%s)' % (jid, sp))
            kt = json.loads(g.ev("(() => { const e = eventsOn(%d).find(x => x.id === 'sunday-story'), k = placeSpot('4-common-kettle'); if (!e || !k) return JSON.stringify(null); const r = tradSpot({ ...e, day: %d }, k.x, k.z); return JSON.stringify(r ? [r[0].id, r[0].pose || null] : null); })()" % (d, d)))
            check(bool(kt) and str(kt[1] or '').startswith('sit'), '%s: asked from right by the kettle, a seated join still picks a seat (seat-first) (%s)' % (jid, kt))
        if 'err' in st: check(False, '%s: someone at it to join (%s)' % (jid, st['err'])); g.close(); continue
        if jid in SEATED:   # RV14's q_seat: a seated weekend join puts you in a seat (tradSpot's seat-first), not standing (the Sunday story had you at the kettle)
            if st['free'] == 0: print('  %s: every seat in its room taken, so you stand beside them (the game\'s own fallback, its words say so): %s' % (jid, st['seat']))
            else: check(st['seat'][1] == 'sit' and str(st['seat'][2] or '').startswith('sit'), '%s: you join in a seat, sitting, with %d free (place, its pose, yours: %s)' % (jid, st['free'], st['seat']))
        best = st['n0']; ended = None
        for k in range(200):
            g.step(60); x = json.loads(g.ev("JSON.stringify([SHIP.time.min, ACT ? ACT.kind : null, SHIP.player.needs['%s']])" % st['need']))
            best = max(best, x[2])
            if x[1] != 'tj:' + jid: ended = x[0]; break
            if x[0] > r['to'] + 5: break
        check(st['act'] == 'tj:' + jid and ended is not None and ended <= r['to'] + 3 and best > st['n0'] + 5,
              '%s: a tap-join starts, ends by itself (%s, its end %d) and gives its %s (%.0f -> %.0f)' % (jid, round(ended) if ended else None, r['to'], st['need'], st['n0'], best))
        g.close()
    # RV14's q_seat, the rule itself (the showings above are often full, so the join's own fallback stands you beside them): on each
    # seated one's day, every place counted free, standing at its nearest standing spot (the Sunday story's kettle), the join picks a seat
    g = Game(pw, won, 900, 760)
    for jid, d in sorted([(i, d) for i, d in TRADS.items() if i in SEATED], key=lambda x: x[1]):
        q = json.loads(g.ev("""(() => { const d = %d, e = eventsOn(d).find(x => x.id === '%s'); if (!e) return JSON.stringify({ err: 'not on' });
          const w = (e.ev.where || [])[0]; skipTo((d - 1) * 1440 + e.from + 10); goToDeck(w.deck, null); SHIP.device.settings.tips = false; e.rooms = e.rooms || eventRooms(e.ev);
          const E = { ...e, day: d }, ids = [...tradSpotIds(E)], st = ids.map(id => [id, placeSpot(id)]).filter(([, sp]) => sp && sp.pose !== 'sit');
          const goals = DECK_CREW.map(a => a.goalId), busy = [...BUSY]; for (const a of DECK_CREW) a.goalId = null; BUSY.clear();   // (heldBy reads goalId; put back below)
          let r; try { const at = st[0] && st[0][1], got = at ? tradSpot(E, at.x, at.z) : null; r = { stand: st.map(x => x[0]), seats: ids.length - st.length, got: got && got[0].id, pose: got && got[1].pose }; }
          finally { DECK_CREW.forEach((a, k) => { a.goalId = goals[k]; }); for (const b of busy) BUSY.add(b); }
          return JSON.stringify(r); })()""" % (d, jid)))
        if 'err' in q: check(False, '%s: on Day %d (%s)' % (jid, d, q['err'])); continue
        if not q['stand']: print('  %s: no standing spot among its places (%d seats): nothing to prefer a seat over' % (jid, q['seats'])); continue
        check(q['pose'] == 'sit', "RV14's q_seat: %s, every place free, from its standing spot %s: the join picks a seat (%s, %s)" % (jid, q['stand'][0], q['got'], q['pose']))
    check(not g.errors, 'no errors: ' + ' | '.join(g.errors[:5]))
    g.close()
    g = Game(pw, won, 900, 760)
    # ---- Bread day (Day 7, Sunday) ----
    g.ev("(() => { skipTo(6 * 1440 + 428); goToDeck(3, null); player.obj.position.set(37 - OX, 0, 8.5 - OZ); SHIP.device.settings.tips = false; })()")
    g.step(420)   # to about 07:16: Cook-along's spots (FX9) are a few steps further from the galley door than the old 3-bread-* ones
    b = json.loads(g.ev("JSON.stringify({ dress: dressingOn(), crew: DECK_CREW.filter(a => a.settled && a.spot && /^3-cookalong-/.test(a.spot.id)).length })"))
    check('breadDay' in b['dress'], 'Bread day: flour, dough and tins on the prep island (%s)' % b['dress'])
    check(b['crew'] >= 3, 'Bread day: crew kneading round the island (%d)' % b['crew'])
    j = json.loads(g.ev("(() => { const e = eventsOn(7).find(x => x.id === 'bread-day'), a = DECK_CREW.find(x => x.p.id === 'brennan'); tradJoin({ ...e, day: 7 }, a); return JSON.stringify({ act: ACT && ACT.kind }); })()"))
    check(j['act'] == 'tj:bread-day', 'Bread day: you join and knead (%s)' % j['act'])
    while g.ev("SHIP.time.min") < 476: g.step(60)
    check(g.ev("SHIP.weekend.loaf") == 7 and g.ev("!ACT || ACT.kind !== 'tj:bread-day'"), 'Bread day: it ends, and your loaf is noted for Monday')
    g.ev("(() => { skipTo(7 * 1440 + 420); goToDeck(3, null); })()"); g.step(30)
    check('loafCard' in g.ev("dressingOn()"), 'Monday 07:00: your loaf in the breakfast basket')
    g.ev("(() => { skipTo(8 * 1440 + 420); })()"); g.step(30)
    check('loafCard' not in g.ev("dressingOn()") and 'breadDay' not in g.ev("dressingOn()"), 'Tuesday: no loaf, no flour')
    g.close()
    # ---- T5 decor (FX16): the picnic's basket (Day 20, 13:20) and the cocoa pot (Day 27, 22:50) while they're on, gone after ----
    g = Game(pw, won, 900, 760)
    for dd, deck, m, did in [(20, 3, 800, 'picnicBasket'), (27, 3, 1370, 'cocoaPot')]:
        g.ev("(() => { skipTo(%d * 1440 + %d - 1440); goToDeck(%d, null); SHIP.device.settings.tips = false; })()" % (dd - 1, m, deck)); g.step(30)
        before = did in g.ev("dressingOn()")
        g.ev("(() => { skipTo(%d * 1440 + %d); goToDeck(%d, null); })()" % (dd - 1, m, deck)); g.step(30)
        on_ = did in g.ev("dressingOn()"); calls = g.ev("renderer.info.render.calls")
        g.ev("(() => { skipTo(%d * 1440 + %d + 120); })()" % (dd - 1, m)); g.step(30)
        after = did in g.ev("dressingOn()")
        check(not before and on_ and not after, 'T5 decor: %s on Day %d only while it\'s on (day before %s, on %s, two hours later %s; draw calls %s)' % (did, dd, before, on_, after, calls))
    check(not g.errors, 'no errors: ' + ' | '.join(g.errors[:5]))
    g.close()
    # ---- The big jigsaw (Day 21, Sunday afternoon; Day 20 the same room is as before) ----
    g = Game(pw, won, 900, 760)
    g.ev("(() => { skipTo(19 * 1440 + 830); goToDeck(1, null); })()"); g.step(30)
    check('bigJigsaw' not in g.ev("dressingOn()"), 'Saturday: no jigsaw on the conference table')
    g.ev("(() => { skipTo(20 * 1440 + 815); goToDeck(1, null); player.obj.position.set(4.5 - OX, 0, 3.5 - OZ); SHIP.device.settings.tips = false; })()")
    g.step(240)
    jz = json.loads(g.ev("JSON.stringify({ dress: dressingOn(), crew: DECK_CREW.filter(a => a.settled && a.spot && a.spot.room === 'O').length })"))
    check('bigJigsaw' in jz['dress'] and jz['crew'] >= 3, 'Sunday 13:35: the jigsaw on the table, %d crew at it' % jz['crew'])
    t = json.loads(g.ev("(() => { const e = eventsOn(21).find(x => x.id === 'big-jigsaw'), a = DECK_CREW.find(x => x.spot && x.spot.room === 'O'); tradJoin({ ...e, day: 21 }, a); return JSON.stringify({ act: ACT && ACT.kind, mins: ACT ? Math.round(ACT.o.end - shipNow()) : null }); })()"))
    check(t['act'] == 'tj:big-jigsaw' and t['mins'] == 20, 'the jigsaw: a turn is 20 minutes (%s)' % t)
    while g.ev("SHIP.time.min") < 845: g.step(60)
    check(g.ev("!ACT || ACT.kind !== 'tj:big-jigsaw'"), 'the jigsaw: your turn ends after its 20 minutes')
    while g.ev("SHIP.time.min") < 935: g.step(60)
    check(g.ev("SHIP.player.hobbies.done.puzzle || 0") >= 1, 'the jigsaw counts as your puzzles hobby')
    g.ev("(() => { skipTo(20 * 1440 + 960); })()"); g.step(30)
    check('bigJigsaw' not in g.ev("dressingOn()"), 'after 15:45: the jigsaw is put away')
    check(not g.errors, 'no errors: ' + ' | '.join(g.errors[:5]))
    g.close()
    # ---- The Sunday story (FX9): Holt reads the showing's chapter in his bubble, story.sunday.1 on Day 28, .2 on Day 56 (a chapter a showing: the rotation) ----
    g = Game(pw, won, 900, 760)
    for d, ch in [(28, 1), (56, 2)]:
        g.ev(f"""(() => {{ skipTo(({d} - 1) * 1440 + 1278); goToDeck(4, null); SHIP.device.settings.tips = false; window.__said = [];
          if (!window.__bsHook) {{ window.__bsHook = 1; const bs = bubbleSay; bubbleSay = function (who, text, secs) {{ if (who && who.p) window.__said.push([who.p.id, text]); return bs.apply(this, arguments); }}; }} }})()""")   # (hooked once)
        g.step(10)
        g.ev(f"(() => {{ const e = eventsOn({d}).find(x => x.id === 'sunday-story'); if (!e) return; const rk = [...eventRooms(e.ev)].map(r => r.split('|')).find(r => +r[0] === 4)[1], tl = ROOM_TILES[rk], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.set(c.x, 0, c.z); player.stop(); }})()")   # (in its room: at 21:18 Holt may still be on his way in)
        for _ in range(60):   # to near its end (21:55): the chapter is spread over what's left once he's settled
            g.step(30)
            if g.ev('SHIP.time.min') >= 1312: break
        r = json.loads(g.ev(f"JSON.stringify({{ holt: DECK_CREW.some(x => x.p.id === 'holt'), said: window.__said.filter(x => x[0] === 'holt').map(x => x[1]), want: (LINES['story.sunday.{ch}'] || []).map(x => x.text) }})"))
        print('  the Sunday story, Day %d: Holt here %s, said %d lines, chapter %d has %d' % (d, r['holt'], len(r['said']), ch, len(r['want'])))
        check(r['holt'] and r['said'] == r['want'], 'the Sunday story on Day %d: Holt reads chapter %d from its first line, every line in order once (RV14) (%s)' % (d, ch, r['said'][:2]))
    check(not g.errors, 'no errors: ' + ' | '.join(g.errors[:5]))
    g.close()
print('WEEKEND CHECK OK' if ok else 'WEEKEND CHECK FAILED')
sys.exit(0 if ok else 1)
