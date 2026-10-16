# Starship Cadet: events check (keep in the repo, next to day_check.py)
# Steps a few weeks of ship days with ?nosave and checks the ship's small traditions (section 18, SHIP_TRADITIONS):
#   each event happens when it's due (its weekday, every N days, its day of the year, a birthday) and on no other day;
#   people go to it (an occasional day with nobody, the room full of others, is noted; never anyone fails), only at its time (honorees a little early; staying on up to 25 minutes after) and only to its places;
#   the schedules stay sound on event days (dayReport: sleep, meals, shifts, no double-booking, no gaps);
#   the same day planned twice gives the same events;
#   on the deck, minute by minute through each event (the CrewAgents, no drawing): attendees reach their places,
#   nobody is stuck for more than 10 ship minutes, nobody shares a place; draw calls at the event under BUDGET;
#   the Mail the evening before (18:00), once each; decor on the deck while it's on, and gone after;
#   the player joining by being in the room (a little social, once); the tap line before it;
#   a ship-wide event on paper: the ion storm's skeleton from day 10, its phases in order, eventMod in each, the same twice.
# Setup and environment as for cadet_test.py.
# Run:  python3 events_check.py BUILD.html [DAYS]     (DAYS defaults to 28, from Day 1, plus days 100 and 300)
import sys
exec(open(__file__.replace('events_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

DAYS = int(sys.argv[2]) if len(sys.argv) > 2 else 28
BUDGET = 450
STEP = 0.05                    # real seconds a step, as day_check

PLANS = r"""(days => {
  const out = { days: [], bad: [], empty: [], ids: SHIP_TRADITIONS.map(e => e.id) }, LINGER = 25;   // staying on a little after the end is fine
  const tagId = tag => { const m = /^ev-(.+?)(-(talk|drink|play|water|wash|read))?$/.exec(tag); return m && m[1]; };
  for (const d of days) {
    const on = eventsOn(d), wd = weekday(d), yd = shipYearDay(d), row = { d, wd: WEEKDAYS[wd].slice(0, 3), ev: [] };
    // due exactly when the table says
    for (const ev of SHIP_TRADITIONS) {
      const w = ev.when, due = w.birthday ? schedPeople().some(p => birthdayOf(p) === yd) : (w.weekday === wd || (w.every && d % w.every === w.on) || w.yearDay === yd);
      if (due !== on.some(e => e.id === ev.id)) out.bad.push(d + ' ' + ev.id + (due ? ' due but not on' : ' on but not due'));
    }
    const S = schedData(), went = {}, places = {};
    for (const p of schedPeople()) for (const s of planDay(p, d)) {
      if (!s.tag || !/^ev-/.test(s.tag)) continue;
      const id = tagId(s.tag), e = on.find(x => x.id === id), B = (d - 1) * 1440;
      if (!e) { out.bad.push(d + ' ' + p.id + ' at ' + id + ', which is not on'); continue; }
      if (s.from < B + e.from - (e.ev.early || 0) || s.to > B + e.to + LINGER) out.bad.push(d + ' ' + p.id + ' at ' + id + ' ' + hhmm(s.from - B) + '-' + hhmm(s.to - B) + ' outside ' + hhmm(e.from) + '-' + hhmm(e.to));
      const pools = eventOpts(e.ev, p).map(([n, k]) => S.shared.get(n + '|' + k) || []).flat().map(pl => pl.id);
      if (!pools.includes(s.placeId)) out.bad.push(d + ' ' + p.id + ' at ' + id + ' in ' + s.placeId + ', not one of its places');
      (went[id] = went[id] || new Set()).add(p.id); (places[id] = places[id] || new Set()).add(s.placeId);
    }
    for (const e of on) {
      const want = schedPeople().filter(p => eventPlan(p, d).some(x => x.id === e.id)).length, n = went[e.id] ? went[e.id].size : 0;
      const cap = new Set(e.ev.where.flatMap((w, i) => S.shared.get(w.deck + '|' + (w.room ? 'ev:' + e.id + ':' + i : w.pool)) || []).map(pl => pl.id)).size;
      if (!n) out.empty.push(d + ' ' + e.id + ': nobody went (' + want + ' meant to; the room was full)');
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
        eventsTick(); window.__skip = false; window.__step(1, 1); window.__step(2, 16); setShipNow(now);   // settled: the cutaway's fades done
        r.calls = renderer.info.render.calls; r.crew = DECK_CREW.length; r.decor = EV_DECOR.g ? EV_DECOR.g.children.length : 0;
      }
    }
    r.reached = mine.filter(([i]) => got.has(i)).length;
    r.notReached = mine.filter(([i]) => !got.has(i)).map(([i, s]) => i + '>' + s.placeId + ' ' + hhmm(s.from - B)).slice(0, 6);
    out.decks.push(r);
  }
  return out;
})"""


# a ship-wide event on paper (Pillar 3): the ion storm's skeleton from day 10, stepped every 10 ship minutes to day 15,
# twice from a clean slate. Phases in order, eventMod right in each phase, the end logged with a band and traces.
STORM = r"""(() => {
  const run = () => {
    const keep = { e: SHIP.event, log: SHIP.eventLog.slice(), tr: SHIP.traces.slice() };
    SHIP.event = null; SHIP.eventLog.length = 0; SHIP.traces.length = 0;
    eventStart('ionStorm', 10); EV_DAYS.clear();
    const a0 = ADDRESSES.length, mails = [], ms = MEETINGS.length, send = typeof mailSend === 'function' ? mailSend : null;
    if (send) mailSend = m => { mails.push(Math.floor(m.at / 1440) + 1 + ' ' + hhmm(m.at % 1440) + ' ' + m.subject); };
    const news = [], fmt = x => Math.floor(x.born / 1440) + 1 + ' ' + hhmm(x.born % 1440) + ' ' + x.id + ' (' + x.seed.length + ' know): ' + x.lines[0];
    const real = typeof NEWS !== 'undefined' && typeof newsAdd === 'function', n0 = real ? (socInit(), NEWS.length) : 0;   // section 20's own, or a stand-in
    if (!real) window.newsAdd = x => { news.push(fmt(x)); return x; };
    const on = [10, 11, 13, 16].map(d => { const o = eventOn(d); return d + ':' + (o ? o.day + ' ' + o.phases.map(p => p.id + '@' + p.from).join(' ') : '-'); });
    const gath = [10, 13].map(d => eventGatherings(d).map(g => d + ' ' + g.id + ' ' + g.where + ' ' + hhmm(g.at) + ' ' + g.len).join('; '));
    const steps = [], sig = [], mods = {};
    const paused = [9, 10, 11, 12, 13, 14].map(d => d + ':' + eventsOn(d).map(e => e.id).join('+'));
    for (let t = 9 * 1440; t <= 17 * 1440; t += 10) {
      const n = eventNow(t);
      const o = eventAdvance(t, true); if (o.length) steps.push('day ' + (Math.floor(t / 1440) + 1) + ' ' + hhmm(t % 1440) + ' ' + o.join(', '));
      const k = n ? n.phase : '-', m = [eventMod('wear', 'power', t), eventMod('wear', 'comms', t), eventMod('effect', 'flicker', t)];
      sig.push(k + ':' + m.join(',')); mods[k] = m;
      if (n && n.phase === 'escalation') eventScore('blackout', 1);   // a stand-in: a minute of blackout per step of the escalation
      const g = eventMod('galley', 'menu', t); if (g) mods.menu = g;
    }
    if (send) mailSend = send;
    if (real) { for (const x of NEWS.splice(n0)) { news.push(fmt(x)); delete SHIP.knows[x.id]; } } else delete window.newsAdd;
    const addr = ADDRESSES.slice(a0).map(x => Math.floor(x.at / 1440) + 1 + ' ' + hhmm(x.at % 1440) + ' ' + x.text);
    const meets = MEETINGS.slice(ms).map(m => m.id + ' day ' + (Math.floor(m.at / 1440) + 1) + ' ' + hhmm(m.at % 1440) + ' ' + m.script);
    ADDRESSES.length = a0; MEETINGS.length = ms; EV_DAYS.clear();
    const res = { steps, sig: sig.join('|'), mods, log: JSON.parse(JSON.stringify(SHIP.eventLog)), traces: SHIP.traces.slice(), left: SHIP.event, addr, mails, meets, paused, news, on, gath,
      scripts: Object.keys(MEETING_SCRIPTS), lines: Object.values(MEETING_SCRIPTS).map(sc => sc.lines.length), modAfter: eventMod('wear', 'power', 12 * 1440) };
    SHIP.event = keep.e; SHIP.eventLog.length = 0; SHIP.eventLog.push(...keep.log); SHIP.traces.length = 0; SHIP.traces.push(...keep.tr);
    return res;
  };
  const a = run(), b = run();
  return { a, same: a.sig === b.sig && JSON.stringify(a.log) === JSON.stringify(b.log) && a.addr.join() === b.addr.join() && a.mails.join() === b.mails.join(), due: eventDueDay(), cal: upcomingTraditions(0, 7 * 1440).slice(0, 3) };
})()"""

# a live ion storm (0.34.9): started on day 10 and played through on the deck at the moments that matter: Calder's
# briefing in the Works bay (the panel, the cast, a choice), the front at 14:00 on day 11 (the jolt, the address), the
# all-clear in the observation room (walking out mails the gist), then on to the end (the log, the traces, the debrief)
LIVE = r"""(() => {
  const dress = [], hadDress = typeof dressShow === 'function', ds = hadDress ? dressShow : null;
  window.dressShow = l => { const k = l.map(x => typeof x === 'string' ? x : x.id + (x.lines ? '[' + x.lines.length + ']' : '')).join('+'); if (dress[dress.length - 1] !== k) dress.push(k); };
  const D = {}, mails = [], send = mailSend; mailSend = m => { mails.push(Math.floor(m.at / 1440) + 1 + ' ' + hhmm(m.at % 1440) + ' ' + m.subject); };
  const keep = { e: SHIP.event, log: SHIP.eventLog.slice(), tr: SHIP.traces.slice() };
  SHIP.event = null; SHIP.eventLog.length = 0; SHIP.traces.length = 0; MEETINGS.length = 0; FEEL.log.length = 0; FEEL_DONE.clear();
  const put = (n, id) => { if (deckDef.num !== n) goToDeck(n); const at = DECKS[n].places.find(p => p.id === id).at;
    player.obj.position.copy(cellPos(...nearestOpen(...cellPos(...at).toArray().filter((_, i) => i !== 1), player))); target.copy(player.obj.position).setY(.7); };
  const tick = (a, b) => { for (let t = a; t <= b; t++) { setShipNow(t); eventsTick(); } };
  const frames = () => { window.__skip = false; window.__step(1, 1); window.__step(2, 16); return renderer.info.render.calls; };
  skipTo(9 * 1440 + 7 * 60); eventStart('ionStorm', 10); EV_DAYS.clear(); eventAdvance(shipNow(), true);
  // the briefing: day 10, 08:15, the Works bay
  put(5, '5-jobboard-1'); tick(9 * 1440 + 7 * 60 + 50, 9 * 1440 + 8 * 60 + 16);
  D.briefing = DIALOGUE ? { open: true, cast: Object.fromEntries(Object.entries(DIALOGUE.cast).map(([k, p]) => [k, p.name])), first: dialogueView() } : { open: false };
  D.panel = !!(DIALOGUE_EL && !DIALOGUE_EL.hidden && DIALOGUE_EL.textContent.length > 5);
  D.calls1 = frames();
  const seen = []; let n = 0;
  while (DIALOGUE && n++ < 30) { const v = dialogueView(); seen.push((v.choices ? '[choice] ' + v.choices.join(' / ') : v.name + ': ' + v.text)); dialogueStep(v.choices ? 0 : undefined); }
  D.lines = seen; D.mine = { ...SHIP.event.mine }; D.closed = !DIALOGUE;
  // the front: day 11, 14:00, on Deck 3
  skipTo(10 * 1440 + 13 * 60 + 50); put(3, '3-grab-1'); tick(10 * 1440 + 13 * 60 + 51, 10 * 1440 + 14 * 60 + 1);
  D.feel = FEEL.log.map(f => f.kinds.join('+')); D.banner = !!(ADDRESS_EL && !ADDRESS_EL.hidden); D.flicker = FEEL.flicker; D.calls2 = frames();
  // the all-clear: day 13, 10:00, the observation room; then walk out to the bridge
  skipTo(12 * 1440 + 9 * 60 + 50); put(1, '1-tea-1'); tick(12 * 1440 + 9 * 60 + 51, 12 * 1440 + 10 * 60 + 1);
  D.allClear = DIALOGUE ? dialogueView() : null; D.calls3 = frames();
  put(1, '1-works-1'); tick(12 * 1440 + 10 * 60 + 2, 12 * 1440 + 10 * 60 + 2); D.walked = !DIALOGUE;
  skipTo(15 * 1440 + 10);
  D.log = JSON.parse(JSON.stringify(SHIP.eventLog)); D.traces = SHIP.traces.slice(); D.left = SHIP.event; D.mails = mails;
  D.dress = dress; if (hadDress) window.dressShow = ds; else delete window.dressShow;
  mailSend = send; SHIP.event = keep.e; SHIP.eventLog.length = 0; SHIP.eventLog.push(...keep.log); SHIP.traces.length = 0; SHIP.traces.push(...keep.tr);
  MEETINGS.length = 0; EV_DAYS.clear(); if (DIALOGUE) dialogueEnd(true); if (ADDRESS_EL) ADDRESS_EL.hidden = true;
  return D;
})()"""

# occasions (C10, 0.34.11): a commendation on day 16 -> the ready-room summons on day 17 at 11:00 (the door open, the
# meeting played in the room, kept), the Captain's table on day 20 (booked the day before, the galley's batch, missed),
# a progress talk asked for on day 18, and nothing booked without a commendation
OCC = r"""(() => {
  const R = {}, mails = [], send = mailSend; mailSend = m => { mails.push(Math.floor(m.at / 1440) + 1 + ' ' + hhmm(m.at % 1440) + ' ' + m.subject); };
  const keep = { o: SHIP.occasions.slice(), c: SHIP.commendations.slice(), e: SHIP.event, tr: SHIP.traces.slice() };
  SHIP.occasions.length = 0; SHIP.commendations.length = 0; SHIP.event = null; MEETINGS.length = 0;
  const tick = (a, b) => { for (let t = a; t <= b; t++) { setShipNow(t); eventsTick(); } };
  skipTo(16 * 1440 + 360); R.none = SHIP.occasions.length;
  SHIP.commendations.push({ event: 'ionStorm', day: 16 });
  skipTo(16 * 1440 + 400); R.booked = SHIP.occasions.map(r => r.key + ' ' + hhmm(r.at % 1440) + ' ' + r.status);
  R.doorBefore = occasionDoorOpen(1, 'R', 16 * 1440 + 600); R.doorAt = occasionDoorOpen(1, 'R', 16 * 1440 + 655);
  skipTo(16 * 1440 + 640); goToDeck(1); const b = ROOM_BOX.R;   // inside the ready room (its door is section 14's doorOpenFor, not in yet)
  player.obj.position.copy(cellPos(Math.floor((b.i0 + b.i1) / 2), Math.floor((b.j0 + b.j1) / 2))); target.copy(player.obj.position).setY(.7);
  R.room = roomAt(...player.here());
  tick(16 * 1440 + 641, 16 * 1440 + 661);
  R.open = DIALOGUE ? DIALOGUE.id : null; const seen = []; let n = 0;
  while (DIALOGUE && n++ < 20) { const v = dialogueView(); seen.push(v.choices ? '[choice]' : v.who + ': ' + v.text); dialogueStep(v.choices ? 2 : undefined); }
  R.lines = seen; tick(16 * 1440 + 662, 16 * 1440 + 690);
  R.after = SHIP.occasions.map(r => r.key + ' ' + r.status);
  R.ask = !!occasionAsk('progressTalk', 17 * 1440 + 840); R.askOff = !!occasionAsk('progressTalk', 21 * 1440 + 840);   // day 22 is a Monday: Calder's off
  skipTo(18 * 1440 + 900); R.table = SHIP.occasions.map(r => r.key + ' ' + hhmm(r.at % 1440) + ' ' + r.status);
  R.batch = eventMod('galley', 'batch', 19 * 1440 + 900); R.noBatch = eventMod('galley', 'batch', 18 * 1440 + 900);
  skipTo(20 * 1440 + 60); R.end = SHIP.occasions.map(r => r.key + ' ' + r.status); R.mails = mails; R.traces = SHIP.traces.slice();
  mailSend = send; SHIP.occasions.length = 0; SHIP.occasions.push(...keep.o); SHIP.commendations.length = 0; SHIP.commendations.push(...keep.c);
  SHIP.event = keep.e; SHIP.traces.length = 0; SHIP.traces.push(...keep.tr); MEETINGS.length = 0; if (DIALOGUE) dialogueEnd(true);
  return R;
})()"""

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev("window.__realTick = tickShip; tickShip = () => {}")
    g.ev("player.steer = null; player.stop()")
    print(f"{g.ev('SHIP_TRADITIONS.length')} events: " + ', '.join(g.ev("SHIP_TRADITIONS.map(e => e.id)")))
    days = list(range(1, DAYS + 1)) + [100, 300]

    # 1. on paper: due days, who goes, where, and the schedules
    r = g.ev(f"({PLANS})({days})")
    for row in r['days']:
        if row['ev']:
            print(f"Day {row['d']} {row['wd']}: " + '; '.join(f"{e['id']}{' (' + e['names'] + ')' if e['names'] else ''} {e['at']} went {e['went']}/{e['want']} (places {e['cap']})" for e in row['ev']))
    seen = {e['id'] for row in r['days'] for e in row['ev'] if e['went']}
    for x in r['empty']: print('  note:', x)
    for i in r['ids']:
        if i not in seen: fail(f"{i} never happened (or nobody ever went) in the days checked")
    for b in r['bad'][:20]: fail(b)
    if len(r['bad']) > 20: print(f"  ... and {len(r['bad']) - 20} more")
    same = g.ev(f"({SAME})(4)")
    print('Plans the same twice (day 4):', same)
    if not same: fail('day 4 planned differently the second time')

    # 2. on the deck: one of each kind, walked through minute by minute
    bd = g.ev(f"[...Array({DAYS}).keys()].map(i => i + 1).find(d => eventsOn(d).some(e => e.id === 'birthday'))")
    sims = [(1, 'running'), (6, 'observatory-night'), (4, 'quiz'), (5, 'works-tea'), (5, 'jam'), (bd, 'birthday'), (6, 'film'), (6, 'harvest'), (7, 'market'), (24, 'hull-lights'), (100, 'founding'), (300, 'quiet-watch')]
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
        g.ev(f"SHIP.galley = null; goToDeck(3); setShipNow(({d} - 1) * 1440 + eventsOn({d}).find(e => e.id === '{i}').from + 10); if (typeof galleyTick === 'function') galleyTick(); EV_MIN = -1; eventsTick()")
        on = g.ev("EV_DECOR.g ? EV_DECOR.g.children.length : 0")
        if k == 'cake':                                   # one cake: the galley's on the servery (section 16) when it's out, else ours
            gc = g.ev("typeof evGalleyCake === 'function' && evGalleyCake()")
            print(f"  the galley's cake out: {gc}; ours: {on} meshes")
            if gc and on: fail('two cakes: the galley\'s and ours')
            if gc or g.ev("typeof galleyAdvance === 'function'"): on = 1   # the galley bakes it (0.29.15)
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


    # 5. a ship-wide event on paper: the ion storm's skeleton, twice
    st = g.ev(STORM); a = st['a']
    print('Ion storm on paper (days 10-16):'); [print('  ' + x) for x in a['steps']]
    print(f"  wear and flicker by phase: {a['mods']}; result {a['log'][0]['band'] if a['log'] else '-'}, threads {a['log'][0]['threads'] if a['log'] else '-'}, traces {a['traces']}")
    print('  addresses:'); [print('    ' + x) for x in a['addr']]
    print('  Mail:', a['mails'])
    print('  meetings:', a['meets'], '| scripts', a['scripts'], a['lines'])
    print('  traditions by day (storm from day 10):', a['paused'], '| menu', a['mods'].get('menu'))
    print('  news:'); [print('    ' + x) for x in a['news']]
    print('  eventOn:', a['on'], '| gatherings:', a['gath'])
    print('  the same twice:', st['same'], '| due in play:', st['due'], '(None while the storm is a draft)')
    print('  upcoming traditions:', [(c['title'], c['at'], c['where']) for c in st['cal']])
    want = ['start', 'warning', 'onset', 'escalation', 'resolution', 'afterglow', 'end']
    got = [w for x in a['steps'] for w in want if (' ' + w) in (' ' + x.split(' ', 3)[3]).replace('phase ', ' ').replace('end ', ' end ')]
    if [w for w in want if w != 'start'] != [w for w in got if w != 'start']: fail(f"storm phases out of order: {a['steps']}")
    m = a['mods']
    if m.get('-') != [None, None, None] or m.get('onset') != [1.5, 2, True] or m.get('escalation') != [2, 3, True] or m.get('resolution') != [None, None, None]: fail(f"eventMod by phase: {m}")
    if not st['same']: fail('the storm ran differently the second time')
    if len(a['addr']) != 2 or 'in it' not in a['addr'][0] or 'passed' not in a['addr'][1]: fail(f"the Captain's addresses: {a['addr']}")
    if not any('Storm prep' in x for x in a['mails']) or not any('how it went' in x for x in a['mails']): fail(f"the storm's Mail: {a['mails']}")
    if len(a['news']) != 7 or not all('@10 ' in x for x in a['news']): fail(f"the storm's news: {a['news']}")
    if a['on'] != ['10:0 warning@360', '11:1 warning@0 onset@840', '13:3 escalation@0 resolution@600 afterglow@1320', '16:-'] or 'stormBriefing works-bay 08:15' not in a['gath'][0] or 'party bow-lounge 19:00' not in a['gath'][1]: fail(f"eventOn / eventGatherings: {a['on']} {a['gath']}")
    if len(a['meets']) != 2: fail(f"the storm's meetings: {a['meets']}")
    if m.get('menu') != 'stormStew': fail('eventMod at t: no storm stew in the escalation')
    if a['log'] and 'calls' not in a['log'][0]['threads']: fail('the call-home backlog was not scored')
    pd = dict(x.split(':') for x in a['paused'])
    if 'quiz' in pd['11'] or 'works-tea' in pd['12']: fail(f"traditions in the storm: {a['paused']}")
    if len(a['log']) != 1 or a['log'][0]['band'] not in ('smooth', 'bumpy', 'rough') or a['left'] is not None: fail(f"the storm didn't end cleanly: {a['log']} {a['left']}")
    if not st['cal']: fail('upcomingTraditions found nothing in the first week')

    # 6. a live ion storm on the deck
    L = g.ev(LIVE)
    print('Live ion storm:')
    print('  briefing:', L['briefing'], '| panel shown:', L['panel'], '| draw calls', L['calls1'])
    [print('    ' + x) for x in L['lines']]
    print('  after it:', {k: v for k, v in L['mine'].items()}, '| closed:', L['closed'])
    print('  the front:', L['feel'], '| address banner:', L['banner'], '| flicker on:', L['flicker'], '| draw calls', L['calls2'])
    print('  all-clear:', L['allClear'], '| draw calls', L['calls3'], '| walked out, closed:', L['walked'])
    print('  Mail:', L['mails'])
    print('  log:', L['log'], '| traces', L['traces'])
    print('  dressing shown:', L['dress'])
    if not any('signupWorks[3]' in x for x in L['dress']) or not any('partyLounge' in x for x in L['dress']): fail(f"the storm's dressing: {L['dress']}")
    b = L['briefing']
    if not b['open'] or set(b.get('cast', {})) != {'calder', 'tech1', 'tech2'} or not L['panel']: fail(f"the briefing didn't open with its cast: {b}")
    if not any(x.startswith('[choice]') for x in L['lines']) or not any('Mind the lift' in x for x in L['lines']) or not L['closed']: fail('the briefing script did not play through with the reply')
    if L['mine'].get('choice:calderStorm') != 1 or not (L['mine'].get('wants:stormBatteries') or L['mine'].get('jobs')): fail(f"the briefing choice was not recorded: {L['mine']}")
    if any('Storm briefing (notes)' in x for x in L['mails']): fail('a gist was mailed for a briefing played to the end')
    if not L['feel'] or 'jolt' not in L['feel'][0] or not L['banner'] or not L['flicker']: fail('the front was not felt (jolt, banner, flicker)')
    if not L['allClear'] or L['allClear']['name'] != 'Captain Odile Marrow' or not L['walked'] or not any('The all-clear (notes)' in x for x in L['mails']): fail('the all-clear did not open, or walking out sent no gist')
    if max(L['calls1'], L['calls2'], L['calls3']) >= 450: fail('draw calls over 450 in the storm')
    if len(L['log']) != 1 or L['left'] is not None or not L['traces'] or not any('how it went' in x for x in L['mails']): fail(f"the live storm didn't end cleanly: {L['log']}")

    # 7. occasions (C10)
    O = g.ev(OCC)
    print('Occasions: before a commendation', O['none'], '| booked', O['booked'], '| door', O['doorBefore'], O['doorAt'], '| in room', O['room'])
    print('  ready room:', O['open'], O['lines'])
    print('  after:', O['after'], '| progress talk asked:', O['ask'], 'on a day off:', O['askOff'])
    print('  the table:', O['table'], '| batch', O['batch'], O['noBatch'], '| end', O['end'], '| traces', O['traces'])
    print('  Mail:', O['mails'])
    if O['none'] or not O['booked'] or 'readyRoom@17 11:00 asked' not in O['booked'][0] or O['doorBefore'] or not O['doorAt']: fail(f"the ready-room summons: {O['booked']}")
    if O['open'] != 'readyRoomFirst' or not any('Admiral' in x for x in O['lines']) or 'readyRoom@17 kept' not in O['after']: fail(f"the ready room didn't play or wasn't kept: {O['open']} {O['after']}")
    if not O['ask'] or O['askOff']: fail('occasionAsk: the progress talk')
    if not any('captainsTable@20 19:30' in x for x in O['table']) or not O['batch'] or O['noBatch']: fail(f"the Captain's table: {O['table']} {O['batch']}")
    if not any('captainsTable@20 missed' in x for x in O['end']) or 'framedMenu' in O['traces'] or not any('Captain\'s table (notes)' in x for x in O['mails']): fail(f"a missed table: {O['end']} {O['mails']}")

    if g.errors: fail(f"console: {g.errors[:4]}")
    g.b.close()

print('EVENTS CHECK OK' if ok else 'EVENTS CHECK FAILED')
sys.exit(0 if ok else 1)
