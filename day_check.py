# Starship Cadet: day check (keep in the repo, next to cadet_test.py and deck_check.py)
# Fast-forwards one whole ship day with ?nosave and checks, deterministically:
#   the schedules (dayReport): everyone sleeps at least 6 hours in their own bed, eats twice and works their
#   whole shift; no place is held by two people at once; no gaps in anyone's day
#   the crew on every deck, minute by minute (the CrewAgents, with no drawing): nobody stuck for more than 10 ship
#   minutes; nobody settles in a place someone else is settled in; nobody lies in a bed that isn't theirs;
#   nobody is left with no way to their place; everyone whereIs puts on the deck is there (or on the way)
#   draw calls: a frame drawn every ship hour on every deck, by the lift and over the crowd, peak under BUDGET
#   the same start gives the same day: the plans, and Deck 4's crew at the end of the day, twice over
#   rooms in use over the week (every place type, with those nobody used listed) and the crew's needs through the day
# Setup and environment as for cadet_test.py.
# Run:  python3 day_check.py BUILD.html [DAY]     (DAY defaults to 1, a Monday)
import sys, json
exec(open(__file__.replace('day_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

DAY = int(sys.argv[2]) if len(sys.argv) > 2 else 1
BUDGET = 450
STEP = 0.05                    # real seconds a step (the main loop's longest frame): 0.03 ship minutes at SHIP_RATE 0.6

# run one deck through the day: the crew logic only, a step at a time; every ship hour, draw a frame or two
SIM = r"""(async ({ n, day, step, draw }) => {
  const B = (day - 1) * 1440, perMin = Math.round(1 / (step * SHIP_RATE)), perHour = perMin * 60, out = { deck: n, stuck: 0, stuckWho: '', shared: 0, sharedWho: [], notOwnBed: [], noPath: [], missing: 0, peakCrew: 0, calls: [], unexpected: [] };
  setShipNow(B); goToDeck(n);
  const LL = typeof LINE_LOG === 'object' ? LINE_LOG : null;   // the servery line (0.26.30): counted afresh for this deck
  if (LL) for (const k in LL) LL[k] = Array.isArray(LL[k]) ? [] : 0;
  out.trayOut = 0; out.trayWho = []; out.trayStill = 0; out.stillWho = []; const still = new Map();
  const own = new Map(schedPeople().map(p => [p.id, p.bed]));
  for (let k = 0; B + k * step * SHIP_RATE < B + 1440; k++) {
    setShipNow(B + k * step * SHIP_RATE);
    updateDeckCrew(step);
    const now = shipNow(), held = new Map();
    for (const a of DECK_CREW) {
      if (a.stuckMax > out.stuck) { out.stuck = a.stuckMax; out.stuckWho = a.p.id + ' ' + hhmm(now - B); }
      if (a.noPath && !out.noPath.includes(a.p.id)) out.noPath.push(a.p.id);
      if (a.hold === 'tray' && roomAt(...a.here()) !== 'M') { out.trayOut++; if (out.trayWho.length < 6) out.trayWho.push(a.p.id + ' ' + hhmm(now - B)); }   // a tray only in the mess hall
      if (a.hold !== 'tray' || a.settled && a.spot && a.spot.pose === 'sit') still.delete(a.p.id);   // standing still a ship minute with a tray, not sat down
      else { const s = still.get(a.p.id); if (!s || Math.hypot(s.x - a.x, s.z - a.z) > .05) still.set(a.p.id, { x: a.x, z: a.z, t: now });
        else if (now - s.t >= 1 && !s.n) { s.n = 1; out.trayStill++; if (out.stillWho.length < 6) out.stillWho.push(a.p.id + ' ' + hhmm(now - B) + ' ' + a.goalId); } }
      if (a.settled && a.spot) {
        if (held.has(a.spot.id)) { out.shared++; const w = a.spot.id + ' ' + held.get(a.spot.id) + '/' + a.p.id; if (out.sharedWho.length < 6 && !out.sharedWho.some(x => x.startsWith(w))) out.sharedWho.push(w + ' from ' + hhmm(now - B)); }
        held.set(a.spot.id, a.p.id);
        if (a.spot.pose === 'lie' && PLACE_OF.get(a.spot.id) && PLACE_OF.get(a.spot.id).type === 'bed' && a.spot.id !== own.get(a.p.id)) out.notOwnBed.push(a.p.id + ' in ' + a.spot.id);
      }
    }
    out.peakCrew = Math.max(out.peakCrew, DECK_CREW.length);
    if (k % perMin === 0) {                                   // every ship minute: is everyone due here here?
      const here = new Set(DECK_CREW.map(a => a.p.id));
      for (const p of schedPeople()) { const w = whereIs(p, now); if (w.deck === n && w.act !== 'commute' && now - w.from > 1 && !here.has(p.id)) out.missing++; }
    }
    if (draw && k % perHour === 0) {                         // every ship hour: a frame by the lift and one over the crowd
      for (const view of ['lift', 'crowd']) {
        let c = view === 'lift' ? cellPos(...nearestOpen(LIFT_AT[0], LIFT_AT[1], player)) : null;
        if (!c) { if (!DECK_CREW.length) continue; c = new THREE.Vector3(DECK_CREW.reduce((s, a) => s + a.x, 0) / DECK_CREW.length, 0, DECK_CREW.reduce((s, a) => s + a.z, 0) / DECK_CREW.length); }
        player.obj.position.copy(c); target.copy(c).setY(.7);
        window.__skip = false; window.__step(1, 1);         // one real frame through the main loop (it also ticks the clock a hair)
        out.calls.push([hhmm(now - B), view, renderer.info.render.calls, DECK_CREW.length]);
      }
      setShipNow(B + k * step * SHIP_RATE);
    }
  }
  out.line = LL ? JSON.parse(JSON.stringify(LL)) : null;
  out.end = DECK_CREW.map(a => [a.p.id, Math.round(a.x * 1000), Math.round(a.z * 1000), a.pose]).sort().join('|');
  return out;
})"""

ok = True
def fail(msg):
    global ok
    ok = False
    print('  FAIL', msg)

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    # stop the game's own loop from moving anything between our steps: we drive the crew ourselves
    g.ev("window.__realTick = tickShip; tickShip = () => {}")
    g.ev("player.steer = null; player.stop()")
    print(f"Day {DAY} ({g.ev(f'WEEKDAYS[weekday({DAY})]')}), {g.ev(f'schedPeople().filter(p => aboard(p, {DAY})).length')} people aboard ({g.ev(f'schedPeople().filter(p => p.guest && aboard(p, {DAY})).length')} of them guests)")

    # 1. the schedules
    r = g.ev(f"dayReport({DAY})")
    print('Schedules:', 'sleep < 6 h', len(r['short']), '| meals < 2', len(r['meals']), '| shift short', len(r['work']), '| double-booked', len(r['double']), '| gaps', len(r['gaps']))
    for k in ('short', 'meals', 'work', 'double', 'gaps'):
        if r[k]: fail(f"{k}: {r[k][:8]}")
    print('  peak headcount by deck:', ', '.join(f"{d}: {v[0]} at {v[1]}" for d, v in sorted(r['peak'].items())))
    if r['unplaced']: print('  moments with no place (standing about):', r['unplaced'])

    # rooms in use: every place type over the week from DAY (types nobody used are listed, not failed)
    rooms = g.ev(f"roomsInUse({DAY}, 7)")
    unused = [x['k'] for x in rooms if not x['uses']]
    few = [f"{x['k']} ({x['people']})" for x in rooms if x['uses'] and x['people'] < 3]
    print(f"Rooms in use over the week from day {DAY}: {len(rooms) - len(unused)} of {len(rooms)} place types (deck and type) used")
    print('  never used:', ', '.join(unused) or 'none')
    print('  used by fewer than 3 people:', ', '.join(few) or 'none')
    # crew needs on paper through the day (lowest and middle value of each)
    nd = g.ev(f"""(() => {{ const out = []; for (const hm of [390, 720, 1140, 1380]) {{ const all = schedPeople().filter(p => aboardAllDay(p, {DAY})).map(p => crewNeeds(p, ({DAY} - 1) * 1440 + hm));
      out.push(hhmm(hm) + '  ' + NEEDS.map(k => {{ const v = all.map(n => n[k]).sort((a, b) => a - b); return k + ' ' + v[0] + '/' + v[v.length >> 1]; }}).join('  ')); }} return out; }})()""")
    print('Crew needs (lowest/middle):'); [print('  ' + l) for l in nd]
    # energy at the end of the day (0.73.0, playtest 2: nobody, you included, ends a day at 0 by default play): the crew at
    # 23:59 on paper, and you awake from 06:00 at full energy to midnight, on shift if it's a workday for you
    en = g.ev(f"""(() => {{ const B = ({DAY} - 1) * 1440, crew = schedPeople().filter(p => aboardAllDay(p, {DAY})).map(p => [crewNeeds(p, B + 1439).energy, p.id]).sort((a, b) => a[0] - b[0]);
      const n = SHIP.player.needs, keep = {{ ...n }}, out = {{ crewLow: crew[0] }}; Object.assign(n, NEEDS_FRESH, {{ energy: 100 }});
      const shift = typeof playerShiftOn === 'function' && playerShiftOn({DAY}), wl = typeof WORK_LEISURE !== 'undefined' ? WORK_LEISURE : 0;
      for (let m = 360; m < 1440; m++) {{ needsDrain(1, false); if (shift && m >= DAY_SHIFT[0] && m < DAY_SHIFT[1]) n.leisure = needClamp(n.leisure - wl / 60); if (m === 22 * 60) out.you22 = Math.round(n.energy); }}
      out.you24 = Math.round(n.energy); out.leisure = Math.round(n.leisure); out.shift = shift; Object.assign(n, keep); return out; }})()""")
    print('Energy at the end of the day: crew lowest', en['crewLow'], '| you (no meals, nothing): at 22:00', en['you22'], 'at midnight', en['you24'], '| leisure', en['leisure'], '| your workday', en['shift'])
    if en['crewLow'][0] <= 0: fail(f"someone ends the day with no energy: {en['crewLow']}")
    if en['you22'] <= 0 or en['you24'] <= 0: fail(f"you end the day with no energy: {en}")
    # a crew-change day: where each leaver waits in the shuttle bay from 14:30. The spot is one of Deck 5's
    # shuttle-bay crowd places, picked by the leaver's id (bay[strSeed(id) % count]), so it moves whenever the bay's
    # crowd places change (the walkable Tern, decks 0.38.19: 120 -> 108 places). A plan difference here alone is expected
    lv = g.ev(f"""(() => schedPeople().filter(p => !p.guest && crewLeaving(p) === {DAY}).map(p => {{ const w = planWhere(p, ({DAY} - 1) * 1440 + 885);
      return p.id + ' ' + (w && w.placeId || '-'); }}).join(', '))()""")
    if lv: print('Leavers waiting in the shuttle bay at 14:45 (the spot follows the bay\'s crowd places):', lv)

    # 1b. the Commons first (the rec deck's crew, RA 0.83; plan v5 section 9): Deck 3's evening count (17:00-24:00, from the
    # plans) beside the rec deck's, against the same build with the REC_DECK switch off. The rec deck's everyday use (the
    # build with its traditions switched off, REC_TRAD_ON) must never leave the Commons with fewer people than without the
    # deck, minute by minute; its traditions (gatherings, exempt from the cap like talent night) are reported beside it. The
    # rec deck holds at most REC_CAP outside gatherings
    rec = g.ev("typeof REC_DECK !== 'undefined' ? REC_DECK : null")
    if rec is not None:
        src = pathlib.Path(sys.argv[1]).read_text()
        on_src = src.replace('const REC_DECK = false;', 'const REC_DECK = true;', 1)
        off_src = on_src.replace('const REC_DECK = true;', 'const REC_DECK = false;', 1)
        bare_src = on_src.replace('const REC_TRAD_ON = REC_DECK;', 'const REC_TRAD_ON = false;', 1)
        if off_src == on_src: print('The Commons and the rec deck: no REC_DECK line to flip')
        else:
            COUNT = f"""(() => {{ const sd = shipDay({DAY}), h = Array.from(sd.occ.heads.slice(1020, 1440)), r = sd.occ.rec ? Array.from(sd.occ.rec.slice(1020, 1440)) : null;
              // at a gathering (or riding to and from one: the ride is counted on the deck)
              const gath = r ? Array.from({{ length: 420 }}, (_, i) => schedPeople().filter(p => planDay(p, {DAY}).some(s => s.deck === 7 && /^ev-/.test(s.tag || '') && s.from - 5 <= ({DAY} - 1) * 1440 + 1020 + i && s.to + 5 > ({DAY} - 1) * 1440 + 1020 + i)).length) : null;
              return {{ h, r, gath, cap: typeof REC_CAP !== 'undefined' ? REC_CAP.busy : null, trads: eventsOn({DAY}).filter(e => /^rec-/.test(e.id)).map(e => e.id) }}; }})()"""
            res = {}
            for k, text in (('on', on_src), ('off', off_src), ('bare', bare_src)):
                if text == src: res[k] = g.ev(COUNT); continue
                f = WORK / 'test' / ('_rec_' + k + '_' + pathlib.Path(sys.argv[1]).name); f.write_text(text)
                g2 = Game(pw, str(f)); res[k] = g2.ev(COUNT); g2.close()
            on, off, bare = res['on'], res['off'], res['bare']
            mean = lambda l: sum(l) / max(1, len(l))
            print(f"The Commons and the rec deck, 17:00-24:00 (from the plans): Deck 3 mean {mean(off['h']):.1f} peak {max(off['h'])} without the rec deck;"
                  f" {mean(bare['h']):.1f} / {max(bare['h'])} with its everyday use; {mean(on['h']):.1f} / {max(on['h'])} with its traditions too ({', '.join(on['trads']) or 'none today'})")
            if on['r'] and bare['r']: print(f"  the rec deck: mean {mean(on['r']):.1f} peak {max(on['r'])} (everyday use alone: mean {mean(bare['r']):.1f} peak {max(bare['r'])})")
            if not on['r'] or not bare['r'] or max(bare['r']) == 0: fail('the rec deck is on but nobody came to it in the evening (no rec counts): the comparison would prove nothing')   # R6
            lower = [i for i in range(420) if bare['h'][i] < off['h'][i]]
            if lower: fail(f"the Commons hold fewer with the rec deck's everyday use at {len(lower)} minutes, first {1020 + lower[0]} ({bare['h'][lower[0]]} v {off['h'][lower[0]]})")
            if on['r'] and on['cap']:
                over = [i for i in range(420) if on['r'][i] - on['gath'][i] > on['cap']]
                if over: fail(f"the rec deck over its cap of {on['cap']} outside gatherings at {len(over)} minutes")

    # 2. the same start gives the same plans
    a = g.ev(f"(() => {{ SHIP_DAYS.clear(); return JSON.stringify(schedPeople().map(p => planDay(p, {DAY}))); }})()")
    b = g.ev(f"(() => {{ SHIP_DAYS.clear(); shipDay({DAY} + 3); shipDay({DAY} - 1); return JSON.stringify(schedPeople().map(p => planDay(p, {DAY}))); }})()")
    print('Plans the same twice:', a == b)
    if a != b: fail('plans differ between runs')
    # the Works crew's 13:00 tea and biscuits (0.71.1, X): on Deck 5 only between WORKS_TEA.at and .until, at most the
    # tea corner's seats at once, and nobody in Works on Deck 5 has a tea outside it; most of those at work go
    wt = g.ev(f"""(() => {{ if (typeof WORKS_TEA === 'undefined') return null; const B = ({DAY} - 1) * 1440, out = {{ on: 0, went: 0, outside: [], peak: 0 }}, at = new Map();
      for (const p of schedPeople().filter(p => p.dept === 'works' && p.shift !== 'night' && p.work && p.work.deck === 5)) {{
        const segs = planDay(p, {DAY}); if (!segs.some(s => s.act === 'work')) continue; out.on++;
        const tea = segs.filter(s => s.tag === 'tea' && s.deck === 5); if (tea.length) out.went++;   // posted to another deck that day: their own tea there
        for (const s of tea) {{ if (s.from < B + WORKS_TEA.at || s.to > B + WORKS_TEA.until + WORKS_TEA.wait) out.outside.push(p.id + ' ' + hhmm(s.from - B)); for (let m = s.from; m < s.to; m++) at.set(m, (at.get(m) || 0) + 1); }}
      }}
      out.peak = Math.max(0, ...at.values()); return out; }})()""")
    print('Works tea at 13:00:', wt)
    if wt and (wt['outside'] or wt['peak'] > 3 or (wt['on'] and wt['went'] < wt['on'] // 3)): fail(f'Works tea wrong: {wt}')

    # the morning (the user's playtest 2, 0.71.5): the day shift wakes spread out from 05:30, not all go straight to
    # breakfast (some work out, some have a coffee or a read first), and every one of them eats breakfast and is at
    # work by 09:00 (the galley rota and the night shift have their own mornings)
    mo = g.ev(f"""(() => {{ const B = ({DAY} - 1) * 1440, out = {{ n: 0, wake: {{}}, first: {{}}, late: [], noBreakfast: [] }};
      for (const p of schedPeople()) {{
        if (p.shift === 'night' || !p.work || !isWorkDay(p, {DAY}) || (galleyRotaOn() && p.dept === 'galley') || !aboardAllDay(p, {DAY}) || (shiftBlocks(p, {DAY}) || {{}}).blocks) continue;   // a rota of their own (the store, the galley): dayReport checks those
        const segs = planDay(p, {DAY}), w = segs.find(s => s.act === 'work'); if (!w) continue; out.n++;
        const sl = segs.filter(s => s.act === 'sleep' && s.from < B + 600).pop(), wk = sl ? sl.to - B : 0, h = hhmm(Math.floor(wk / 30) * 30);
        out.wake[h] = (out.wake[h] || 0) + 1;
        const f = segs.find(s => s.from >= B + wk && !['sleep', 'commute', 'off'].includes(s.act) && !['toilet', 'lift', 'inspection'].includes(s.tag));
        const k = !f ? 'none' : f.act === 'breakfast' ? 'breakfast' : f.act === 'gym' ? 'workout' : f.act === 'wash' ? (segs.some(s => s.from > f.from && s.act === 'leisure' && s.from < (segs.find(x => x.act === 'breakfast') || {{ from: Infinity }}).from) ? 'wash, then a coffee or read' : 'wash') : f.act;
        out.first[k] = (out.first[k] || 0) + 1;
        if (w.from > B + SHIFTS.day[0]) out.late.push(p.id + ' ' + hhmm(w.from - B));
        if (!segs.some(s => s.act === 'breakfast')) out.noBreakfast.push(p.id + (habitsOn(p, {DAY}).includes('skips-breakfast') ? ' (skips)' : ''));
      }}
      return out; }})()""")
    print('Mornings of the day shift:', mo['n'], '| woke', dict(sorted(mo['wake'].items())), '| first thing', mo['first'])
    if mo['late']: fail(f"late to the shift: {mo['late'][:8]}")
    if [x for x in mo['noBreakfast'] if not x.endswith('(skips)')]: fail(f"no breakfast: {mo['noBreakfast'][:8]}")

    # 3. every deck through the day
    decks = g.ev("typeof DECK_ORDER !== 'undefined' ? DECK_ORDER.slice().sort((a, b) => a - b) : Object.keys(DECKS).map(Number)")
    for n in decks:
        o = g.page.evaluate(f"s => window.__sc(s)({{ n: {n}, day: {DAY}, step: {STEP}, draw: true }})", SIM)
        peak = max([c[2] for c in o['calls']] or [0])
        print(f"Deck {n}: up to {o['peakCrew']} crew, worst stuck {o['stuck']:.1f} ship min ({o['stuckWho']}), draw calls peak {peak} (budget {BUDGET})")
        busiest = sorted(o['calls'], key=lambda c: -c[2])[:2]
        print('  busiest frames:', ', '.join(f"{c[0]} {c[1]} {c[2]} calls, {c[3]} crew" for c in busiest))
        if o['stuck'] > 10: fail(f"deck {n}: {o['stuckWho']} stuck {o['stuck']:.1f} ship minutes")
        if o['shared']: fail(f"deck {n}: two people settled in one place {o['shared']} times: {o['sharedWho']}")
        if o['notOwnBed']: fail(f"deck {n}: in someone else's bed: {sorted(set(o['notOwnBed']))[:6]}")
        if o['noPath']: fail(f"deck {n}: no way to their place: {o['noPath'][:8]}")
        if o['missing']: fail(f"deck {n}: someone due on the deck wasn't there ({o['missing']} person-minutes)")
        if peak > BUDGET: fail(f"deck {n}: {peak} draw calls")
        L = o.get('line')
        if L and L['joined']:
            print(f"  servery line: {L['joined']} joined, {L['served']} served, longest {L['long']}, longest wait {L['wait']:.1f} ship min, trays {L.get('trays', 0)}, gone with the meal {L['returned']}, gave up {L['left']} {L['who']}")
            if L['left']: fail(f"deck {n}: {L['left']} gave up on the servery line: {L['who']}")
        if o['trayStill']: fail(f"deck {n}: standing still with a tray {o['trayStill']} times: {o['stillWho']}")
        if o['trayOut']: fail(f"deck {n}: a tray outside the mess hall {o['trayOut']} times: {o['trayWho']}")

    # jobs (section 17): the machine panels and other places the crew's jobs took them to, from the day just run
    jv = g.ev("typeof jobVisits === 'function' ? jobVisits() : null")
    if jv is not None:
        print('Job visits (jobs on the books after the day):', ', '.join(f"{x['k']}: {x['visits']} at {x['places']}" for x in jv) or 'none')

    # 4. the same day twice on the crew's own deck (both runs without drawing: a drawn frame also runs the game's loop)
    o1 = g.page.evaluate(f"s => window.__sc(s)({{ n: 4, day: {DAY}, step: {STEP}, draw: false }})", SIM)
    o2 = g.page.evaluate(f"s => window.__sc(s)({{ n: 4, day: {DAY}, step: {STEP}, draw: false }})", SIM)
    print('Deck 4 the same twice:', o1['end'] == o2['end'])
    if o1['end'] != o2['end']: fail('Deck 4 came out differently the second time')

    # 5. the arrival on (section 21's intro, off in every test URL): day 0 and Monday's beats laid over the plans never
    # put two people in one place at once (reviewer 1: Calder and Torres both at 5-stool-1 for Monday's briefing)
    ia = g.ev(r"""(() => { if (typeof newGameStart !== 'function' || typeof introBeats !== 'function') return null;
      newGameStart(true); const dbl = [];
      for (const d of [0, 1]) for (const [id, L] of shipDay(d).occ) if (Array.isArray(L)) for (let i = 0; i < L.length; i++) for (let j = i + 1; j < L.length; j++)
        if (L[i][0] < L[j][1] && L[j][0] < L[i][1] && L[i][2] !== L[j][2]) dbl.push(id + ' ' + L[i][2] + '/' + L[j][2] + '@' + (L[j][0] - (d - 1) * 1440));
      return dbl; })()""")
    print('Arrival on, days 0 and 1, places booked twice:', 'no arrival here' if ia is None else ia[:6] or 'none')
    if ia: fail(f'arrival on: places booked twice {ia[:6]}')

    print('errors', g.errors[:5])
    if g.errors: ok = False
    print('DAY CHECK OK' if ok else 'DAY CHECK FAILED')
    g.close()
