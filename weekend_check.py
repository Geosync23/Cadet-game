# Starship Cadet: the weekend traditions check (0.92.5 item 16; FX14's T1-T2, FX11's T3-T4 on; keep in the repo)
# Runs on a copy of the build with WEEKEND_ON switched on (the switch is a URL flag, ?weekend, off in the game):
#   every weekend tradition on its day (eventsOn), and nothing of them with the switch off
#   each join has its activity (PLAYER_ACTS['tj:<id>'], made after the slot adds the joins: tjActs) and a join ends
#   Bread day (T3): crew at the kneading spots (3-bread-*), the island's flour and tins (breadDay), you knead, and your
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
TRADS = {'saturday-run': 6, 'every-song': 6, 'night-owls-cocoa': 6, 'garden-picnic': 6, 'sunday-story': 7, 'gerald-clinic': 14, 'bread-day': 7, 'big-jigsaw': 7}   # a day each is on
DAYS = sorted(set(TRADS.values()))
EVS = "JSON.stringify(%s.map(d => [d, eventsOn(d).map(e => e.id)]))" % json.dumps(DAYS)

with sync_playwright() as pw:
    g = Game(pw, build, 900, 760)
    evs = dict(json.loads(g.ev(EVS)))
    check(not any(i in evs[d] for i, d in TRADS.items()), 'switch off: none of the weekend traditions')
    g.close()
    g = Game(pw, won, 900, 760)
    evs = dict(json.loads(g.ev(EVS)))
    for i, d in TRADS.items(): check(i in evs[d], 'switch on: %s on Day %d' % (i, d))
    acts = json.loads(g.ev("JSON.stringify(Object.keys(TRAD_JOIN).filter(id => WEEKEND_TRADS.has(id) && !TRAD_JOIN[id].act).map(id => [id, !!PLAYER_ACTS['tj:' + id] && typeof PLAYER_ACTS['tj:' + id].until === 'function']))"))
    check(len(acts) >= 7 and all(a for _, a in acts), 'every weekend join has its activity, with an end (%s)' % acts)
    miss = json.loads(g.ev("JSON.stringify([...WEEKEND_TRADS].filter(id => !TRAD_JOIN[id] || (!TRAD_JOIN[id].act && !PLAYER_ACTS['tj:' + id])))"))
    check(not miss, 'every weekend tradition has a join, and each tap-join its activity (missing: %s)' % miss)
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
    g.step(240)
    b = json.loads(g.ev("JSON.stringify({ dress: dressingOn(), crew: DECK_CREW.filter(a => a.settled && a.spot && /^3-bread-/.test(a.spot.id)).length })"))
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
    # ---- The big jigsaw (Day 14, Sunday afternoon; Day 13 the same room is as before) ----
    g = Game(pw, won, 900, 760)
    g.ev("(() => { skipTo(12 * 1440 + 830); goToDeck(1, null); })()"); g.step(30)
    check('bigJigsaw' not in g.ev("dressingOn()"), 'Saturday: no jigsaw on the conference table')
    g.ev("(() => { skipTo(13 * 1440 + 815); goToDeck(1, null); player.obj.position.set(4.5 - OX, 0, 3.5 - OZ); SHIP.device.settings.tips = false; })()")
    g.step(240)
    jz = json.loads(g.ev("JSON.stringify({ dress: dressingOn(), crew: DECK_CREW.filter(a => a.settled && a.spot && a.spot.room === 'O').length })"))
    check('bigJigsaw' in jz['dress'] and jz['crew'] >= 3, 'Sunday 13:35: the jigsaw on the table, %d crew at it' % jz['crew'])
    t = json.loads(g.ev("(() => { const e = eventsOn(14).find(x => x.id === 'big-jigsaw'), a = DECK_CREW.find(x => x.spot && x.spot.room === 'O'); tradJoin({ ...e, day: 14 }, a); return JSON.stringify({ act: ACT && ACT.kind, mins: ACT ? Math.round(ACT.o.end - shipNow()) : null }); })()"))
    check(t['act'] == 'tj:big-jigsaw' and t['mins'] == 20, 'the jigsaw: a turn is 20 minutes (%s)' % t)
    while g.ev("SHIP.time.min") < 845: g.step(60)
    check(g.ev("!ACT || ACT.kind !== 'tj:big-jigsaw'"), 'the jigsaw: your turn ends after its 20 minutes')
    while g.ev("SHIP.time.min") < 935: g.step(60)
    check(g.ev("SHIP.player.hobbies.done.puzzle || 0") >= 1, 'the jigsaw counts as your puzzles hobby')
    g.ev("(() => { skipTo(13 * 1440 + 960); })()"); g.step(30)
    check('bigJigsaw' not in g.ev("dressingOn()"), 'after 15:45: the jigsaw is put away')
    check(not g.errors, 'no errors: ' + ' | '.join(g.errors[:5]))
    g.close()
print('WEEKEND CHECK OK' if ok else 'WEEKEND CHECK FAILED')
sys.exit(0 if ok else 1)
