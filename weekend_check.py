# Starship Cadet: the weekend traditions check (0.92.5 item 16; FX14's T1-T2, FX11's T3-T4 on; keep in the repo)
# Runs on a copy of the build with WEEKEND_ON switched on (the switch is a URL flag, ?weekend, off in the game):
#   every weekend tradition on its day (eventsOn), and nothing of them with the switch off
#   each join has its activity (PLAYER_ACTS['tj:<id>'], made after the slot adds the joins: tjActs) and a join ends
#   Bread day (T3): crew at the kneading spots (Cook-along's 3-cookalong-*), the island's flour and tins (breadDay), you knead, and your
#     loaf is in Monday's breakfast basket (loafCard) 06:30-10:00 and not on Tuesday
#   The big jigsaw (T4): crew at the observation room's table, the puzzle on it (bigJigsaw) only on its Sunday afternoon
#     (Deck 1 as before on other days), a turn is 20 minutes and counts as your puzzles hobby
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
on = re.sub(r"^const WEEKEND_ON = URL_FLAGS\.has\('weekend'\)", "const WEEKEND_ON = true", src, count=1, flags=re.M)
check(on != src, 'the build has the WEEKEND_ON switch')
won = str(WORK / 'test' / ('_weekend_' + pathlib.Path(build).name)); pathlib.Path(won).write_text(on)
TRADS = {'saturday-run': 6, 'bread-day': 7, 'every-song': 69, 'gerald-clinic': 14, 'garden-picnic': 20, 'big-jigsaw': 21, 'night-owls-cocoa': 27, 'sunday-story': 28}   # a day each is on (the 4-week rotation, the user 2026-10-25: two a weekend; Every song's first is Day 69: Day 13 is the storm's lantern supper, and on Day 41 it gives way to a birthday)
DAYS = sorted(set(TRADS.values()))
EVS = "JSON.stringify(%s.map(d => [d, eventsOn(d).map(e => e.id)]))" % json.dumps(DAYS)
# (DS1, the user 2026-10-25: "spread the new ones across weeks, and keep some that were already there") every Saturday and
# Sunday of Days 6-84: the traditions that were already there, with their times, and the new ones on it
WKND = """JSON.stringify((() => { const out = []; for (let d = 6; d <= 84; d++) { if (weekday(d) < 5) continue;
  const L = eventsOn(d); out.push([d, weekday(d), L.filter(e => !WEEKEND_TRADS.has(e.id)).map(e => e.id + ' ' + e.from + '-' + e.to).sort(), L.filter(e => WEEKEND_TRADS.has(e.id)).map(e => e.id)]); } return out; })())"""
# RV14: each weekend tradition's host planned at it, and how many go to each showing of the late ones
HOSTS = """JSON.stringify((() => { const out = []; for (let d = 6; d <= 84; d++) for (const e of eventsOn(d)) { if (!WEEKEND_TRADS.has(e.id)) continue;
  const goers = schedPeople().filter(p => planDay(p, d).some(s => evTagId(s.tag) === e.id)).map(p => p.id);
  const h = e.ev.host && ROSTER.find(p => p.id === e.ev.host), B = (d - 1) * 1440, pl = id => { const n = +String(id).split('-')[0]; return ((DECKS[n] || {}).places || []).find(q => q.id === id); }, room = h && planDay(h, d).some(s => s.placeId && s.from < B + e.to && s.to > B + e.from && pl(s.placeId) && [...(e.rooms || (e.rooms = eventRooms(e.ev)))].includes(s.placeId.split('-')[0] + '|' + pl(s.placeId).room));
  out.push([e.id, d, e.ev.host || null, !!e.ev.host && (goers.includes(e.ev.host) || !!room), goers.length]); } return out; })())"""   # (at it, or at work in its room through it: Brennan cooks in the galley on Bread day)

with sync_playwright() as pw:
    g = Game(pw, build, 900, 760)
    evs = dict(json.loads(g.ev(EVS)))
    check(not any(i in evs[d] for i, d in TRADS.items()), 'switch off: none of the weekend traditions')
    off_w = json.loads(g.ev(WKND))
    g.close()
    g = Game(pw, won, 900, 760)
    evs = dict(json.loads(g.ev(EVS)))
    for i, d in TRADS.items(): check(i in evs[d], 'switch on: %s on Day %d' % (i, d))
    acts = json.loads(g.ev("JSON.stringify(Object.keys(TRAD_JOIN).filter(id => WEEKEND_TRADS.has(id) && !TRAD_JOIN[id].act).map(id => [id, !!PLAYER_ACTS['tj:' + id] && typeof PLAYER_ACTS['tj:' + id].until === 'function']))"))
    check(len(acts) >= 7 and all(a for _, a in acts), 'every weekend join has its activity, with an end (%s)' % acts)
    miss = json.loads(g.ev("JSON.stringify([...WEEKEND_TRADS].filter(id => !TRAD_JOIN[id] || (!TRAD_JOIN[id].act && !PLAYER_ACTS['tj:' + id])))"))
    check(not miss, 'every weekend tradition has a join, and each tap-join its activity (missing: %s)' % miss)
    on_w = json.loads(g.ev(WKND))
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
          const n0 = SHIP.player.needs[need]; tradJoin({ ...e, day: %d }, a); return JSON.stringify({ need, n0, act: ACT && ACT.kind }); })()""" % (d, jid, d, d)))
        if 'err' in st: check(False, '%s: someone at it to join (%s)' % (jid, st['err'])); g.close(); continue
        best = st['n0']; ended = None
        for k in range(200):
            g.step(60); x = json.loads(g.ev("JSON.stringify([SHIP.time.min, ACT ? ACT.kind : null, SHIP.player.needs['%s']])" % st['need']))
            best = max(best, x[2])
            if x[1] != 'tj:' + jid: ended = x[0]; break
            if x[0] > r['to'] + 5: break
        check(st['act'] == 'tj:' + jid and ended is not None and ended <= r['to'] + 3 and best > st['n0'] + 5,
              '%s: a tap-join starts, ends by itself (%s, its end %d) and gives its %s (%.0f -> %.0f)' % (jid, round(ended) if ended else None, r['to'], st['need'], st['n0'], best))
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
          const bs = bubbleSay; bubbleSay = function (who, text, secs) {{ if (who && who.p) window.__said.push([who.p.id, text]); return bs.apply(this, arguments); }}; }})()""")
        g.step(10)
        g.ev(f"(() => {{ const e = eventsOn({d}).find(x => x.id === 'sunday-story'); if (!e) return; const rk = [...eventRooms(e.ev)].map(r => r.split('|')).find(r => +r[0] === 4)[1], tl = ROOM_TILES[rk], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.set(c.x, 0, c.z); player.stop(); }})()")   # (in its room: at 21:18 Holt may still be on his way in)
        g.step(900)
        r = json.loads(g.ev(f"JSON.stringify({{ holt: DECK_CREW.some(x => x.p.id === 'holt'), said: window.__said.filter(x => x[0] === 'holt').map(x => x[1]), want: (LINES['story.sunday.{ch}'] || []).map(x => x.text) }})"))
        print('  the Sunday story, Day %d: Holt here %s, said %d lines, chapter %d has %d' % (d, r['holt'], len(r['said']), ch, len(r['want'])))
        check(r['holt'] and len(r['said']) >= 2 and all(x in r['want'] for x in r['said']), 'the Sunday story on Day %d: Holt reads chapter %d, line by line (%s)' % (d, ch, r['said'][:2]))
    check(not g.errors, 'no errors: ' + ' | '.join(g.errors[:5]))
    g.close()
print('WEEKEND CHECK OK' if ok else 'WEEKEND CHECK FAILED')
sys.exit(0 if ok else 1)
