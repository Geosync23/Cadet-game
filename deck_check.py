# Starship Cadet: deck check (keep in the repo, next to cadet_test.py)
# Visits every built deck with goToDeck and checks, on each:
#   every room tile can be walked to from the lift, every tappable item's approach tile can be reached,
#   (rooms you can't get into at all, like locked cabins and sealed rooms, are listed but not failures;
#   a room you can get into only partly is a failure: something is blocking part of it off)
#   the crew who belong there are active, and draw calls from a fixed view.
#   and, for decks whose definition has `places` (Pillar 1, plans/pillar1-plan.md "Places"): every place's id is unique
#   ship-wide, its type, pose and face come from the agreed lists, its room matches the map, and crew can reach it from
#   the lift (its own tile, or for a seat or bed, a walk-to tile beside it). Crew have keys, so 'closed' doors count as
#   passable for this; hatches, walls and glass don't. A place may name its own walk-to tile (`walk: [c, r]`): then that
#   tile must be walkable, in the same room, reachable from the lift, and `at` itself or within 2.5 m of the spot
#   (`xy: [x, z]` in tile units if given, else the tile centre); it replaces the next-door rule. Counts by type are printed.
#   Pillar 2: service hatches (a deck's `service` list) pass for the player and for Works crew. Room tiles and items are
#   checked as the player walks; `work:works` places may be reached through a service hatch, other places may not.
#   A deck's `machines` ({ id, kind, at, room, face, panel }): ids unique ship-wide, `at` in its room, the panel tile
#   walkable and in the same room, and exactly one place that names it (`machine: id`): a `work:works` place on the
#   panel tile. Every place that names a machine must name one on its deck.
# Then rides 4 -> n -> 4 three times and checks Deck 4's memory comes back to the same counts.
# Setup and environment as for cadet_test.py.
# The game loads with ?nosave&debug (cadet_test.py's Game class), so a save never changes what it checks.
# Run:  python3 deck_check.py BUILD.html
import sys
exec(open(__file__.replace('deck_check.py', 'cadet_test.py')).read().split("a, shots = run(")[0])
from playwright.sync_api import sync_playwright

CHECK = """(() => {
  const start = nearestOpen(LIFT_AT[0], LIFT_AT[1], null);
  const unreachTiles = [], shut = [];
  for (const [room, tiles] of Object.entries(ROOM_TILES)) {
    let n = 0;
    for (const c of tiles) { const ok = K(c) === K(start) || !!findPath(start, c, new Set(), player); if (ok) n++; else unreachTiles.push(room + ':' + c); }
    if (!n) shut.push(room);
  }
  const unreachItems = [];
  for (const it of ITEMS) {
    if (it.lift || it.see) continue;
    const p = new THREE.Vector3(); it.hit.getWorldPosition(p);
    const d = it.depth / 2 + .55, goal = nearestOpen(p.x + Math.sin(it.front) * d, p.z + Math.cos(it.front) * d, player);
    if (!goal || (K(goal) !== K(start) && !findPath(start, goal, new Set(), player))) {
      if (goal && shut.includes(roomAt(...goal))) continue;      // in a room nobody can get into yet
      unreachItems.push(it.t + ' @' + cellAt(p.x, p.z));
    }
  }
  unreachTiles.splice(0, unreachTiles.length, ...unreachTiles.filter(t => !shut.includes(t.split(':')[0])));
  return { tiles: Object.values(ROOM_TILES).reduce((a, t) => a + t.length, 0), items: ITEMS.length, unreachTiles, unreachItems, shut,
    crew: typeof DECK_CREW !== 'undefined' ? [DECK_CREW.length + ' scheduled (' + clockText() + ')'] : crew.filter(c => c.active).map(c => c.spec.name) };
})()"""

# places: reachability for crew (doors, lift doors and 'closed' doors pass; walls, glass and hatches don't, except service
# hatches for work:works places)
PLACES = r"""(() => {
  const ps = deckDef.places; if (!ps) return null;
  const TYPES = ['bed', 'shower', 'basin', 'toilet', 'mess-seat', 'servery-queue', 'grab-shelf', 'gym', 'lounge-seat', 'garden', 'callhome',
    'music', 'bench', 'common-room', 'laundry', 'lift-wait', 'shop'], POSES = ['sit', 'stand', 'lie', 'work'], FACES = ['n', 'e', 's', 'w'];
  const WORKS = { dept: 'works' };
  const passFor = who => (i, j, i2, j2) => { const e = EDGES.get(i2 !== i ? `v,${Math.max(i, i2)},${j}` : `h,${i},${Math.max(j, j2)}`); return !e || !edgeBlocks(e, who) || e.type === 'closed'; };
  const start = nearestOpen(LIFT_AT[0], LIFT_AT[1], null);
  const flood = pass => { const seen = new Set([K(start)]), q = [start];
    while (q.length) { const [i, j] = q.shift(); for (const [di, dj] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const n = [i + di, j + dj];
      if (!seen.has(K(n)) && free(...n) && pass(i, j, ...n)) { seen.add(K(n)); q.push(n); } } }
    return seen; };
  const seenAll = flood(passFor(null)), seenWorks = flood(passFor(WORKS));
  const bad = [], counts = {};
  for (const p of ps) {
    const why = [], works = p.type === 'work:works', seen = works ? seenWorks : seenAll, pass = passFor(works ? WORKS : null);
    if (typeof p.id !== 'string' || !p.id) why.push('no id');
    if (!(TYPES.includes(p.type) || /^work:[a-z-]+$/.test(p.type || ''))) why.push('type ' + p.type);
    if (!POSES.includes(p.pose)) why.push('pose ' + p.pose);
    if (!FACES.includes(p.face)) why.push('face ' + p.face);
    const [c, r] = p.at || [];
    if (roomAt(c, r) !== p.room) why.push('room ' + p.room + ' but the map says ' + roomAt(c, r));
    if (p.xy && !(p.xy.length === 2 && p.xy.every(Number.isFinite))) why.push('xy ' + p.xy);
    if (p.walk) {                                                            // its own walk-to tile
      const [wc, wr] = p.walk, sp = p.xy || [c + .5, r + .5];
      if (!free(wc, wr)) why.push('walk ' + wc + ',' + wr + ' not walkable');
      if (roomAt(wc, wr) !== p.room) why.push('walk in room ' + roomAt(wc, wr));
      if (!seen.has(K([wc, wr]))) why.push('walk unreachable');
      if (!(wc === c && wr === r) && Math.hypot(wc + .5 - sp[0], wr + .5 - sp[1]) > 2.5) why.push('walk too far from the spot');
    } else {
      let ok = seen.has(K([c, r]));
      if (!ok && (p.pose === 'sit' || p.pose === 'lie' || !free(c, r)))    // a seat or bed: reached from the tile beside it
        ok = [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([di, dj]) => seen.has(K([c + di, r + dj])) && pass(c, r, c + di, r + dj));
      if (!ok) why.push('unreachable');
    }
    if (why.length) bad.push(p.id + ' @' + c + ',' + r + ': ' + why.join(', '));
    counts[p.type] = (counts[p.type] || 0) + 1;
  }
  const ms = deckDef.machines || [], mbad = [];
  for (const m of ms) {
    const why = [], [c, r] = m.at || [], [pc, pr] = m.panel || [];
    if (typeof m.id !== 'string' || !m.id) why.push('no id');
    if (typeof m.kind !== 'string' || !m.kind) why.push('no kind');
    if (!['n', 'e', 's', 'w'].includes(m.face)) why.push('face ' + m.face);
    if (roomAt(c, r) !== m.room) why.push('at ' + c + ',' + r + ' is in room ' + roomAt(c, r) + ', not ' + m.room);
    if (roomAt(pc, pr) !== m.room) why.push('panel ' + pc + ',' + pr + ' is in room ' + roomAt(pc, pr));
    if (!free(pc, pr)) why.push('panel ' + pc + ',' + pr + ' not walkable');
    const mine = ps.filter(p => p.machine === m.id);
    if (mine.length !== 1) why.push(mine.length + ' places name it (want 1)');
    else if (mine[0].type !== 'work:works' || !mine[0].at || mine[0].at[0] !== pc || mine[0].at[1] !== pr) why.push('its place ' + mine[0].id + ' is not a work:works place on the panel');
    if (why.length) mbad.push(m.id + ': ' + why.join(', '));
  }
  for (const p of ps) if (p.machine && !ms.some(m => m.id === p.machine)) mbad.push(p.id + ': names machine ' + p.machine + ', not on this deck');
  return { ids: ps.map(p => p.id), bad, counts, n: ps.length, mids: ms.map(m => m.id), mbad };
})()"""

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    decks = g.ev("Object.keys(DECKS).map(Number)")
    ok = True
    allIds = {}
    allMachines = {}
    for n in decks:
        g.ev(f"goToDeck({n})"); g.step(3)
        r = g.ev(CHECK)
        g.ev("player.obj.position.copy(cellPos(...nearestOpen(LIFT_AT[0], LIFT_AT[1], player))); target.copy(player.obj.position).setY(.7)")
        g.step(30)
        calls = g.ev("renderer.info.render.calls")
        print(f"Deck {n}: {r['tiles']} tiles, {r['items']} items, crew {r['crew']}, draw calls by the lift {calls}")
        print(f"  rooms nobody can get into: {''.join(sorted(r['shut']))}")
        for k in ('unreachTiles', 'unreachItems'):
            if r[k]:
                print(f"  {k} ({len(r[k])}): {r[k][:12]}{' ...' if len(r[k]) > 12 else ''}")
                ok = False
        pl = g.ev(PLACES)
        if pl is None: print('  places: none yet')
        else:
            print(f"  places: {pl['n']}  " + ', '.join(f'{t} {c}' for t, c in sorted(pl['counts'].items())))
            for pid in pl['ids']:
                if pid in allIds: print(f"  place id {pid} is used on Deck {allIds[pid]} too"); ok = False
                allIds[pid] = n
            if pl['bad']:
                print(f"  bad places ({len(pl['bad'])}): {pl['bad'][:12]}{' ...' if len(pl['bad']) > 12 else ''}"); ok = False
            if pl['mids']: print(f"  machines: {len(pl['mids'])}")
            for mid in pl['mids']:
                if mid in allMachines: print(f"  machine id {mid} is used on Deck {allMachines[mid]} too"); ok = False
                allMachines[mid] = n
            if pl['mbad']:
                print(f"  bad machines ({len(pl['mbad'])}): {pl['mbad'][:12]}"); ok = False
    mem = []
    for n in [d for d in decks if d != 4] * 3:
        g.ev(f"goToDeck({n})"); g.step(3); g.ev("goToDeck(4)"); g.step(3)
        mem.append(g.ev("JSON.stringify(renderer.info.memory)"))
    print('Deck 4 memory after round trips:', mem)
    if len(set(mem[len(decks) - 1:])) > 1: ok = False; print('  memory changes between round trips')
    print('errors', g.errors)
    if g.errors: ok = False
    print('DECK CHECK OK' if ok else 'DECK CHECK FAILED')
    g.close()
