# Starship Cadet: events check (keep in the repo, next to day_check.py)
# Steps a few weeks of ship days with ?nosave and checks the ship's small traditions (section 18, SHIP_EVENTS):
#   each event happens when it's due (its weekday, every N days, its day of the year, a birthday) and on no other day;
#   people go to it (at least one), only at its time (staying on up to 25 minutes after) and only to its places;
#   the schedules stay sound on event days (dayReport: sleep, meals, shifts, no double-booking, no gaps);
#   the same day planned twice gives the same events;
#   on the deck, minute by minute through each event (the CrewAgents, no drawing): attendees reach their places,
#   nobody is stuck for more than 10 ship minutes, nobody shares a place; draw calls at the event under BUDGET;
#   the Mail the evening before (18:00), once each; decor on the deck while it's on, and gone after;
#   the player joining by being in the room (a little social, once); the tap line before it.
# Setup and environment as for cadet_test.py.
# Run:  python3 events_check.py BUILD.html [DAYS]     (DAYS defaults to 28, from Day 1, plus days 100 and 300)
import sys
exec(open(__file__.replace('events_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 28
BUDGET = 450
STEP = 0.05                    # real seconds a step, as day_check

PLANS = r"""(days => {
  const out = { days: [], bad: [], ids: SHIP_EVENTS.map(e => e.id) }, LINGER = 25;   // staying on a little after the end is fine
  const tagId = tag => { const m = /^ev-(.+?)(-(talk|drink|play|water|wash|read))?$/.exec(tag); return m && m[1]; };
  for (const d of days) {
    const on = eventsOn(d), wd = weekday(d), yd = shipYearDay(d), row = { d, wd: WEEKDAYS[wd].slice(0, 3), ev: [] };
    // due exactly when the table says
    for (const ev of SHIP_EVENTS) {
      const w = ev.when, due = w.birthday ? schedPeople().some(p => birthdayOf(p) === yd) : (w.weekday === wd || (w.every && d % w.every === w.on) || w.yearDay === yd);
      if (due !== on.some(e => e.id === ev.id)) out.bad.push(d + ' ' + ev.id + (due ? ' due but not on' : ' on but not due'));
    }
    const S = schedData(), went = {}, places = {};
    for (const p of schedPeople()) for (const s of planDay(p, d)) {
      if (!s.tag || !/^ev-/.test(s.tag)) continue;
      const id = tagId(s.tag), e = on.find(x => x.id === id), B = (d - 1) * 1440;
      if (!e) { out.bad.push(d + ' ' + p.id + ' at ' + id + ', which is not on'); continue; }
      if (s.from < B + e.from || s.to > B + e.to + LINGER) out.bad.push(d + ' ' + p.id + ' at ' + id + ' ' + hhmm(s.from - B) + '-' + hhmm(s.to - B) + ' outside ' + hhmm(e.from) + '-' + hhmm(e.to));
      const pools = eventOpts(e.ev, p).map(([n, k]) => S.shared.get(n + '|' + k) || []).flat().map(pl => pl.id);
      if (!pools.includes(s.placeId)) out.bad.push(d + ' ' + p.id + ' at ' + id + ' in ' + s.placeId + ', not one of its places');
      (went[id] = went[id] || new Set()).add(p.id); (places[id] = places[id] || new Set()).add(s.placeId);
    }
    for (const e of on) {
      const want = schedPeople().filter(p => eventPlan(p, d).some(x => x.id === e.id)).length, n = went[e.id] ? went[e.id].size : 0;
      const cap = new Set(e.ev.where.flatMap((w, i) => S.shared.get(w.deck + '|' + (w.room ? 'ev:' + e.id + ':' + i : w.pool)) || []).map(pl => pl.id)).size;
      if (!n) out.bad.push(d + ' ' + e.id + ': nobody went (' + want + ' meant to)');
      row.ev.push({ id: e.id, names: e.names, at: hhmm(e.from) + '-' + hhmm(e.to), want, went: n, places: places[e.id] ? places[e.id].size : 0, cap });
    }
    const r = dayReport(d);
    for (const k of ['short', 'meals', 'work', 'double', 'gaps']) if (r[k].length) out.bad.push(d + ' dayReport ' + k + ': ' + r[k].slice(0, 4).join(', '));
    out.days.push(row);
  }
  return out;
})"""

# the same day twice: every event segment, after clearing the caches and planning other days in between
SAME = r"""(d => {
  const sig = () => schedPeople().map(p => planDay(p, d).filter(s => s.tag && /^ev-/.test(s.tag)).map(s => p.id + s.from + s.placeId + s.tag).join()).join('|');
  const a = sig(); SHIP_DAYS.clear(); EV_DAYS.clear(); for (const x of [d + 3, d - 2, d + 1]) shipDay(x); SHIP_DAYS.delete(d);
  return a === sig() && a.length > 0;
})"""

# one event on its deck, minute by minute, from 30 minutes before to its end
SIM = r"""(async ({ d, id, step }) => {
  const e = eventsOn(d).find(x => x.id === id), B = (d - 1) * 1440;
  const att = new Map();                                 // person -> their event segment
  for (const p of schedPeople()) for (const s of planDay(p, d)) if (s.tag && s.tag.startsWith('ev-' + id) && s.placeId) att.set(p.id, s);
  const decks = [...new Set([...att.values()].map(s => s.deck))];
  const out = { id, d, decks: [] };
  for (const n of decks) {
    const r = { n, att: 0, reached: 0, notReached: [], stuck: 0, stuckWho: '', shared: 0, sharedWho: [], noPath: [], calls: 0, crew: 0, decor: 0 };
    const mine = [...att.entries()].filter(([, s]) => s.deck === n); r.att = mine.length;
    const got = new Set();
    SHIP.galley = null;                                  // the galley starts fresh that morning (a jump of weeks has no hover carts)
    setShipNow(B + e.from - 30); goToDeck(n);
    for (let k = 0; B + e.from - 30 + k * step * SHIP_RATE < B + e.to; k++) {
      const now = B + e.from - 30 + k * step * SHIP_RATE; setShipNow(now); updateDeckCrew(step);
      const held = new Map();
      for (const a of DECK_CREW) {
        if (a.stuckMax > r.stuck) { r.stuck = a.stuckMax; r.stuckWho = a.p.id + ' ' + hhmm(now - B); }
        if (a.noPath && !r.noPath.includes(a.p.id)) r.noPath.push(a.p.id);
        if (a.settled && a.spot) {
          if (held.has(a.spot.id)) { r.shared++; if (r.sharedWho.length < 4) r.sharedWho.push(a.spot.id + ' ' + held.get(a.spot.id) + '/' + a.p.id + ' ' + hhmm(now - B)); }
          held.set(a.spot.id, a.p.id);
          const s = att.get(a.p.id); if (s && s.deck === n && now >= s.from && now < s.to && a.spot.id === s.placeId) got.add(a.p.id);
        }
      }
      if (Math.abs(now - (B + e.from + Math.min(30, (e.to - e.from) / 2))) < step * SHIP_RATE / 2 + 1e-9) {   // a frame over the crowd, at the event
        const c = DECK_CREW.length ? new THREE.Vector3(...[...att.keys()].map(i => DECK_CREW.find(a => a.p.id === i)).filter(Boolean).reduce((s, a, _, l) => [s[0] + a.x / l.length, 0, s[2] + a.z / l.length], [0, 0, 0])) : cellPos(...LIFT_AT);
        player.obj.position.copy(c); target.copy(c).setY(.7);
        eventsTick(); window.__skip = false; window.__step(1, 1); setShipNow(now);
        r.calls = renderer.info.render.calls; r.crew = DECK_CREW.length; r.decor = EV_DECOR.g ? EV_DECOR.g.children.length : 0;
      }
    }
    r.reached = mine.filter(([i]) => got.has(i)).length;
    r.notReached = mine.filter(([i]) => !got.has(i)).map(([i, s]) => i + '>' + s.placeId + ' ' + hhmm(s.from - B)).slice(0, 6);
    out.decks.push(r);
  }
  return out;
})"""

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev("window.__realTick = tickShip; tickShip = () => {}")
    g.ev("player.steer = null; player.stop()")
    print(f"{g.ev('SHIP_EVENTS.length')} events: " + ', '.join(g.ev("SHIP_EVENTS.map(e => e.id)")))
    days = list(range(1, DAYS + 1)) + [100, 300]

    # 1. on paper: due days, who goes, where, and the schedules
    r = g.ev(f"({PLANS})({days})")
    for row in r['days']:
        if row['ev']:
            print(f"Day {row['d']} {row['wd']}: " + '; '.join(f"{e['id']}{' (' + e['names'] + ')' if e['names'] else ''} {e['at']} went {e['went']}/{e['want']} (places {e['cap']})" for e in row['ev']))
    seen = {e['id'] for row in r['days'] for e in row['ev']}
    for i in r['ids']:
        if i not in seen: fail(f"{i} never happened in the days checked")
    for b in r['bad'][:20]: fail(b)
    if len(r['bad']) > 20: print(f"  ... and {len(r['bad']) - 20} more")
    same = g.ev(f"({SAME})(4)")
    print('Plans the same twice (day 4):', same)
    if not same: fail('day 4 planned differently the second time')

    # 2. on the deck: one of each kind, walked through minute by minute
    bd = g.ev(f"[...Array({DAYS}).keys()].map(i => i + 1).find(d => eventsOn(d).some(e => e.id === 'birthday'))")
    sims = [(1, 'running'), (2, 'observatory'), (4, 'quiz'), (5, 'works-tea'), (5, 'jam'), (bd, 'birthday'), (6, 'film'), (6, 'harvest'), (7, 'market'), (24, 'hull-lights'), (100, 'founding'), (300, 'quiet-watch')]
    for d, i in sims:
        if not g.ev(f"eventsOn({d}).some(e => e.id === '{i}')"): fail(f"{i} not on day {d}"); continue
        s = g.ev(f"({SIM})({{ d: {d}, id: '{i}', step: {STEP} }})")
        for x in s['decks']:
            print(f"  {i} day {d}, Deck {x['n']}: {x['reached']}/{x['att']} reached their places, worst stuck {x['stuck']:.1f} min {x['stuckWho']}, draw calls {x['calls']} ({x['crew']} crew{', decor ' + str(x['decor']) + ' meshes' if x['decor'] else ''})")
            if x['att'] and x['reached'] < x['att']: (fail if x['reached'] < x['att'] * .8 else print)(f"  not reached: {x['notReached']}")
            if x['stuck'] >= 10: fail(f"stuck {x['stuck']:.1f} min: {x['stuckWho']}")
            if x['shared']: fail(f"places shared: {x['sharedWho']}")
            if x['noPath']: fail(f"no path: {x['noPath']}")
            if x['calls'] >= BUDGET: fail(f"draw calls {x['calls']} >= {BUDGET}")
    for d, i, k in [(7, 'market', 'stalls'), (bd, 'birthday', 'cake')]:
        g.ev(f"goToDeck(3); setShipNow(({d} - 1) * 1440 + eventsOn({d}).find(e => e.id === '{i}').from + 10); EV_MIN = -1; eventsTick()")
        on = g.ev("EV_DECOR.g ? EV_DECOR.g.children.length : 0")
        g.ev(f"setShipNow(({d} - 1) * 1440 + eventsOn({d}).find(e => e.id === '{i}').to + 30); EV_MIN = -1; eventsTick()")
        off = g.ev("EV_DECOR.g ? EV_DECOR.g.children.length : 0")
        print(f"Decor ({k}): {on} meshes during {i}, {off} after")
        if not on or off: fail(f"{k} decor: {on} during, {off} after")

    # 3. the Mail the evening before: a week of skips from Day 1
    g.ev("setShipNow(360); EV_LAST = null; EV_MIN = -1; eventsTick(); SHIP.events.sent.length = 0; EV_MAILBOX.length = 0")
    g.ev("for (let t = 360 + 600; t <= 7 * 1440; t += 600) skipTo(t)")
    m = g.ev("EV_MAILBOX.map(x => [x.event, x.at, x.subject])")
    due = g.ev("[2, 3, 4, 5, 6, 7, 8].flatMap(d => eventsOn(d).map(e => e.id + '@' + d))")
    got = [x[0] for x in m]
    print(f"Mail: {len(m)} announcements for days 2-8 ({len(due)} events due); e.g. {m[0][2] if m else '-'}")
    for k in due:
        if k not in got: fail(f"no Mail for {k}")
    if len(got) != len(set(got)): fail('a Mail sent twice')
    for k, at, _ in m:
        d = int(k.split('@')[1])
        if at != (d - 2) * 1440 + 1080: fail(f"{k} announced at {at}, not 18:00 the evening before")

    # 4. the player joins the quiz by being in the bow lounge (Day 4), and a tap line before it
    line = g.ev("(() => { const p = schedPeople().find(p => planDay(p, 4).some(s => s.tag && s.tag.startsWith('ev-quiz'))); return p ? eventLine(p, 3 * 1440 + 1100) : null; })()")
    print('Tap line before the quiz:', line)
    if not line: fail('no tap line before the quiz')
    j = g.ev("""(() => {
      goToDeck(3); const c = PLACE_OF.get('3-lounge-30'); const at = (DECKS[3].places.find(p => p.id === '3-lounge-30') || {}).at;
      player.obj.position.copy(cellPos(...nearestOpen(...cellPos(...at).toArray().filter((_, i) => i !== 1), player)));
      const n0 = SHIP.player.needs.social = 50; SHIP.events.joined.length = 0;
      for (const m of [1210, 1213, 1217, 1220]) { setShipNow(3 * 1440 + m); EV_MIN = -1; eventsTick(); }
      return { room: roomAt(...player.here()), joined: SHIP.events.joined.slice(), social: SHIP.player.needs.social, n0 };
    })()""")
    print(f"Player in room {j['room']} during the quiz: joined {j['joined']}, social {j['n0']} -> {j['social']}")
    if j['joined'] != ['quiz@4'] or j['social'] <= j['n0']: fail('the player did not join the quiz')

    if g.errors: fail(f"console: {g.errors[:4]}")
    g.b.close()

print('EVENTS CHECK OK' if ok else 'EVENTS CHECK FAILED')
sys.exit(0 if ok else 1)
