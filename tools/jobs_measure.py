# Starship Cadet: jobs measure (JB2, patch 0.99.5 notes 14, 15, 18). Not a pass/fail check: it prints what a steady
# player is offered and takes over DAYS ship days on paper, with the real career (career_check's steady player, but
# the game's own WORK_MECH, so the real training, rounds and side jobs): the jobs by kind, by machine kind, by room and
# deck, how often the washers come up, and each job's length in ship minutes (its holds, a part made at the lathe,
# and the walk from the Works board through each stop and back, at your walking pace, with 2 minutes a lift ride).
# Run:  python3 tools/jobs_measure.py BUILD.html [DAYS] [--json OUT]     (DAYS defaults to 28)
import sys, json, os
sys.argv = [a for a in sys.argv]
exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright
from collections import Counter

DAYS = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 28
OUT = sys.argv[sys.argv.index('--json') + 1] if '--json' in sys.argv else None

PAPER = r"""(({ days }) => {
  const t0 = (SHIP_START.day - 1) * 1440 + SHIP_START.min;
  SHIP.works = null; SHIP.occasions.length = 0; SHIP.notes = []; SHIP.flags = {}; SHIP.jobs = []; SHIP.mail = []; SHIP.rep = null;
  JOBS_ON = true; MACH_HOUR = null; MACH_SEEN = -1; WORKS_TICK.m = WORKS_TICK.h = -1;
  if (typeof eventNow === 'function') { window.__evK = eventNow; eventNow = () => null; }   // ordinary days: no ship-wide events
  const at = t => { setShipNow(t); machinesNow(); };
  const took = [], offered = new Map();
  const info = (j, d) => {
    const m = j.machine && machineById(j.machine), stops = jobStops(j);
    const places = stops.map(s => s.places && s.places[0] || null), decks = stops.map(s => s.deck);
    const ks = jobKindOf(j) ? kindStops(j) : null;
    let hold = ks ? ks.reduce((a, x) => a + (x.mins || 0), 0) : j.kind === 'chore' || j.kind === 'favour' ? (j.stops || []).reduce((a, x) => a + (x.mins || 0), 0) : j.kind === 'restock' ? 33 : jobMins(j);
    if (j.kind !== 'restock' && j.parts && j.parts.length && (ks || j.kind === 'chore' || j.kind === 'favour')) hold += 5;
    else if (m && j.parts && j.parts.length) hold += 5;
    const make = j.make ? makeMins(j) : 0;
    // the walk: Works board -> each stop's place -> the board, at your pace (about 1.78 tiles a real second: player.maxV),
    // 1.7 times the straight line (the median detour of real paths on Deck 4), through the lift (2 ship minutes a ride, the car's 1.8 s and a wait)
    const B = placeById('5-jobboard-1'), xy = pl => pl && pl.at ? [pl.at[0] + .5, pl.at[1] + .5] : null;
    const pts = [[5, xy(B)]].concat(stops.map((s, k) => { const pl = s.places && s.places[0] && placeById(s.places[0]); return pl ? [pl.deck, xy(pl)] : m && k === stops.length - 1 ? [m.deck, m.panel] : s.deck != null ? [s.deck, null] : null; }).filter(Boolean), [[5, xy(B)]]);
    let tiles = 0, rides = 0;
    for (let k = 1; k < pts.length; k++) { const [da, a] = pts[k - 1], [db, b] = pts[k];
      const la = DECKS[da] && DECKS[da].lift, lb = DECKS[db] && DECKS[db].lift, d2 = (p, q) => p && q ? Math.hypot(p[0] - q[0], p[1] - q[1]) : 10;
      if (da === db) tiles += d2(a, b); else { tiles += d2(a, la) + d2(lb, b); rides++; } }
    const deckCh = rides, walk = Math.round(tiles * 1.7 / 1.78 * SHIP_RATE + 2 * rides);
    const rooms = stops.map((s, k) => { const p = s.places && s.places[0] && placeById(s.places[0]); return p ? p.deck + ':' + (roomName(p.deck, p.room) || p.room) : (m && k === stops.length - 1 ? m.deck + ':' + (roomName(m.deck, m.room) || m.room) : null); });
    return { day: d, id: j.id, kind: j.kind, sub: j.chore || j.fix || j.cause || null, title: j.title || null, mkind: m ? m.kind : null, machine: j.machine || null, deck: m ? m.deck : (decks.find(x => x != null) ?? j.deck), rooms, places,
      hold: Math.round(hold), make, walk, total: Math.round(hold + make + walk), stops: stops.length, train: j.train || null, extra: !!j.extra, reserved: j.reserved || null };
  };
  const doJob = id => { const j0 = SHIP.jobs.find(x => x.id === id); if (!j0 || !claimJob(id)) return false; const j = SHIP.jobs.find(x => x.id === id);
    took.push(info(j, SHIP.time.day));
    if (j.train === 'm7' && typeof scanRead === 'function') { scanRead(id); if (typeof caseTick === 'function') caseTick(); }
    const cs = SHIP.works && SHIP.works.cases && (SHIP.works.cases.open || []).find(c => c.job === id);
    if (cs && typeof caseCall === 'function') caseCall(cs.id, cs.cause);
    jobStops(j).forEach((s, k) => { const op = (s.opts && s.opts.options) || s.options;
      if (s.opts && s.opts.marks) { jobStepDone(id, k, { pick: 'fine' }); return; }
      if (!Array.isArray(op)) { jobStepDone(id, k); return; }
      const right = Number.isInteger(j.bad) ? 'x' + j.bad : null, opts = right ? [right].concat(op.map(o => o.id).filter(x => x !== right)) : op.map(o => o.id);
      for (const o of opts) if (jobStepDone(id, k, { pick: o }).ok) break; });
    return turnInJob(id); };
  let busyTill = 0;
  for (let d = 1; d <= days; d++) {
    const work = playerShiftOn(d);
    for (let h = 6; h <= 22; h++) {
      const t = (d - 1) * 1440 + h * 60; at(t);
      worksCareerTick(t);
      if (typeof DIALOGUE !== 'undefined' && DIALOGUE && typeof dialogueEnd === 'function') dialogueEnd(true);
      const W = SHIP.works, c = W && W.cur;
      if (c && c.st === 'meet') { const r = SHIP.occasions.find(x => x.key === c.occ);
        if (r && t >= r.at && t < r.at + r.len + 60) r.met = true;
        if (r && t >= r.at + r.len) occasionsTick(t, true);
        worksCareerTick(t + 1); }
      const c2 = W && W.cur;
      if (c2 && c2.st === 'watch') { c2.w = TRAIN_WATCH; worksCareerTick(t + 2); }
      const shift = work && h >= 8 && h < 17;
      if (shift) for (const o of openJobs('you')) if (!offered.has(o.id)) { const j = SHIP.jobs.find(x => x.id === o.id); if (j) offered.set(o.id, info(j, d)); }
      const c3 = SHIP.works && SHIP.works.cur;
      if (c3 && c3.st === 'do' && shift && !myJob() && t >= busyTill) { const j = SHIP.jobs.find(x => x.id === c3.j); if (j && doJob(c3.j)) busyTill = t + took[took.length - 1].total; worksCareerTick(t + 3); }
      if (shift && !myJob() && t >= busyTill) { const x = openJobs('you')[0]; if (x && doJob(x.id)) busyTill = t + took[took.length - 1].total; }
      if (SHIP.works && work && h === 14) for (const r of CAREER_LADDER) if (r.size === 'big' && SHIP.works.tr[r.id] !== undefined && r.id !== 't2') worksUse(r.id);
      if (SHIP.works && SHIP.works.tr.p3 === undefined && worksOpened().has('p3') && h === 15) worksUse('p3');
      if (SHIP.works && SHIP.works.tr.m2 === undefined && worksOpened().has('m2') && h === 16) worksUse('m2');
    }
  }
  if (window.__evK) eventNow = window.__evK;
  return { took, offered: [...offered.values()], tier: playerTier(), rank: SHIP.works && SHIP.works.rank };
})"""

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    g.ev("if (typeof GUIDE_ON !== 'undefined') GUIDE_ON = false; if (typeof TURN_IN !== 'undefined') TURN_IN = true")
    r = g.ev(PAPER + "({ days: %d })" % DAYS)
    errs = g.errors[:5]
    g.close()

def report(name, L):
    n = len(L)
    print(f"\n== {name}: {n} jobs over {DAYS} days ==")
    if not n: return
    kind = Counter((x['kind'] + (':' + x['sub'] if x['kind'] in ('chore',) and x['sub'] else '')) for x in L)
    print('  by kind:', ', '.join(f"{k} {v}" for k, v in kind.most_common(14)))
    mk = Counter(x['mkind'] or '-' for x in L)
    print('  by machine kind:', ', '.join(f"{k} {v}" for k, v in mk.most_common(14)))
    wash = sum(1 for x in L if x['mkind'] == 'washer' or any(p and 'wash' in p for p in x['places'] if p) or any(rm and 'aundry' in rm for rm in x['rooms'] if rm))
    print(f"  washers / laundry: {wash} ({100 * wash / n:.0f}%)")
    dk = Counter(x['deck'] for x in L)
    print('  by deck (main stop):', ', '.join(f"{k} {v}" for k, v in sorted(dk.items(), key=lambda kv: str(kv[0]))))
    rm = Counter(next((z for z in reversed(x['rooms']) if z), '-') for x in L)
    print(f"  by room (main stop), {len(rm)} rooms:", ', '.join(f"{k} {v}" for k, v in rm.most_common(14)))
    pl = Counter(x['machine'] or next((p for p in reversed(x['places']) if p), '-') for x in L)
    print(f"  distinct spots {len(pl)}; the most visited:", ', '.join(f"{k} {v}" for k, v in pl.most_common(8)))
    T = sorted(x['total'] for x in L)
    print(f"  length (holds + make + rough walk): median {T[n // 2]}, longest {T[-1]}, over 30 min {sum(1 for t in T if t > 30)} ({100 * sum(1 for t in T if t > 30) / n:.0f}%), over 40 min {sum(1 for t in T if t > 40)} ({100 * sum(1 for t in T if t > 40) / n:.0f}%)")
    H = sorted(x['hold'] + x['make'] for x in L)
    print(f"  length without the walk: median {H[n // 2]}, longest {H[-1]}, over 30 {sum(1 for t in H if t > 30)}, over 40 {sum(1 for t in H if t > 40)}")
    longest = sorted(L, key=lambda x: -x['total'])[:8]
    for x in longest: print(f"    Day {x['day']} {x['kind']} {x['sub'] or ''} {x['mkind'] or ''} {x['title'] or ''}: hold {x['hold']} make {x['make']} walk {x['walk']} = {x['total']}")

print('tier at the end', r['tier'], r['rank'], 'errors', errs)
report('Taken by a steady player', r['took'])
report('Offered to you on the board (each once)', r['offered'])
rounds = [x for x in r['took'] if x['kind'] == 'rounds']
print('\nrounds taken:', [(x['day'], x['title'], [p for p in x['places']]) for x in rounds][:12])
if OUT: json.dump(r, open(OUT, 'w'), indent=1)
