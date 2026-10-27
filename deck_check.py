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
#   checked as the player walks; `work:works` and `storage` places (Works errands: parts, carts) may be reached through a
#   service hatch, other places may not.
#   A deck's `machines` ({ id, kind, at, room, face, panel }): ids unique ship-wide, `at` in its room, the panel tile
#   walkable and in the same room, and exactly one place that names it (`machine: id`): a `work:works` place on the
#   panel tile. Every place that names a machine must name one on its deck.
#   The answers pass (0.30.12): a deck's `service` entries are a hatch key or { key, tier } (tier 1, 2 or 3), each one a hatch;
#   a place's `window: true` (a seat by a window) must be a seat or a standing place on a tile beside a hull wall with windows;
#   a deck's `crawl: ['c,r', ...]` tiles must be walkable and reachable for Works crew. Counts are printed.
#   Step 4 (0.53.4): a deck's leak joints stand on free tiles facing a real wall or straight hull, their puddle places free.
# Then rides 4 -> n -> 4 three times and checks Deck 4's memory comes back to the same counts.
# Setup and environment as for cadet_test.py.
# The game loads with ?nosave&debug (cadet_test.py's Game class), so a save never changes what it checks.
# Run:  python3 deck_check.py BUILD.html
import sys, json
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
  const TYPES = ['bed', 'timeclock', 'shower', 'basin', 'toilet', 'mess-seat', 'servery-queue', 'grab-shelf', 'gym', 'lounge-seat', 'garden', 'callhome',
    'music', 'bench', 'common-room', 'laundry', 'lift-wait', 'shop', 'storage', 'event', 'patient-bed', 'bar-staff', 'bar-order', 'shower-queue'], POSES = ['sit', 'stand', 'lie', 'work'], FACES = ['n', 'e', 's', 'w'];
  const WORKS = { dept: 'works', tier: 3, rank: 'senior' };
  const passFor = who => (i, j, i2, j2) => { const e = EDGES.get(i2 !== i ? `v,${Math.max(i, i2)},${j}` : `h,${i},${Math.max(j, j2)}`); return !e || !edgeBlocks(e, who) || e.type === 'closed'; };
  const start = nearestOpen(LIFT_AT[0], LIFT_AT[1], null);
  const flood = pass => { const seen = new Set([K(start)]), q = [start];
    while (q.length) { const [i, j] = q.shift(); for (const [di, dj] of [[1, 0], [-1, 0], [0, 1], [0, -1]]) { const n = [i + di, j + dj];
      if (!seen.has(K(n)) && free(...n) && pass(i, j, ...n)) { seen.add(K(n)); q.push(n); } } }
    return seen; };
  const seenAll = flood(passFor(null)), seenWorks = flood(passFor(WORKS));
  const bad = [], counts = {};
  for (const p of ps) {
    const why = [], works = p.type === 'work:works' || p.type === 'storage' || p.works === true, seen = works ? seenWorks : seenAll, pass = passFor(works ? WORKS : null);
    if (typeof p.id !== 'string' || !p.id) why.push('no id');
    if (!(TYPES.includes(p.type) || /^(work|rec):[a-z-]+$/.test(p.type || ''))) why.push('type ' + p.type);   // rec: the rec deck's player-only places (0.80.1)
    if (!POSES.includes(p.pose)) why.push('pose ' + p.pose);
    if (!FACES.includes(p.face) && !Number.isFinite(p.face)) why.push('face ' + p.face);   // a letter, or any finite degrees from south toward east, e.g. 90 or -145 (sim 0.26.11)
    const [c, r] = p.at || [];
    if (roomAt(c, r) !== p.room) why.push('room ' + p.room + ' but the map says ' + roomAt(c, r));
    if (p.xy && !(p.xy.length === 2 && p.xy.every(Number.isFinite))) why.push('xy ' + p.xy);
    if (p.walk) {                                                            // its own walk-to tile
      const [wc, wr] = p.walk, sp = p.xy || [c + .5, r + .5];
      if (!free(wc, wr)) why.push('walk ' + wc + ',' + wr + ' not walkable');
      if (roomAt(wc, wr) !== p.room) why.push('walk in room ' + roomAt(wc, wr));
      if (!seen.has(K([wc, wr]))) why.push('walk unreachable');
      if (!(wc === c && wr === r) && Math.hypot(wc + .5 - sp[0], wr + .5 - sp[1]) > (p.type === 'rec:seat' ? 4.5 : 2.5)) why.push('walk too far from the spot');   // a rec seat (the auditorium, the stands) is reached along its row from the aisle
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
  const stub = id => typeof machineList === 'function' && machineList().some(m => m.stub && m.id === id && m.deck === deckDef.num);   // a stand-in machine's service place (FX3: the main lift's, at its brake)
  for (const p of ps) if (p.machine && !ms.some(m => m.id === p.machine) && !stub(p.machine)) mbad.push(p.id + ': names machine ' + p.machine + ', not on this deck');
  return { ids: ps.map(p => p.id), bad, counts, n: ps.length, mids: ms.map(m => m.id), mbad };
})()"""

# the answers pass's tags: service tiers, window seats, crawl tiles
TAGS = r"""(() => {
  const bad = [], tiers = {}, WORKS = { dept: 'works', tier: 3, rank: 'senior' };
  for (const sv of deckDef.service || []) {
    const key = typeof sv === 'string' ? sv : sv && sv.key, e = EDGES.get(key);
    if (!e || e.type !== 'hatch' || !e.service) bad.push('service ' + key + ' is not a service hatch');
    if (typeof sv !== 'string') { if (![1, 2, 3].includes(sv.tier)) bad.push('service ' + key + ' tier ' + sv.tier); else tiers[sv.tier] = (tiers[sv.tier] || 0) + 1; }
  }
  const hullBy = (i, j) => [`h,${i},${j}`, `h,${i},${j + 1}`, `v,${i},${j}`, `v,${i + 1},${j}`].some(k => EDGES.get(k) && EDGES.get(k).type === 'hull');
  const winRooms = new Set((deckDef.windows || []).filter(w => w.room).map(w => w.room)), sideWin = (deckDef.windows || []).some(w => w.side);
  let win = 0;
  for (const p of deckDef.places || []) {
    if (p.window === undefined) continue;
    if (p.window !== true) { bad.push(p.id + ': window ' + p.window); continue; }
    const [i, j] = p.at, near = [[0, 0], [1, 0], [-1, 0], [0, 1], [0, -1]].some(([di, dj]) => hullBy(i + di, j + dj));
    if (!['sit', 'stand'].includes(p.pose)) bad.push(p.id + ': a window place, but pose ' + p.pose);
    if (!near || !(winRooms.has(p.room) || sideWin)) bad.push(p.id + ': window, but no hull window beside it');
    win++;
  }
  const crawl = deckDef.crawl || [];
  if (crawl.length) {
    const start = nearestOpen(LIFT_AT[0], LIFT_AT[1], null);
    for (const k of crawl) {
      const [i, j] = String(k).split(',').map(Number);
      if (!/^\d+,\d+$/.test(String(k))) { bad.push('crawl ' + k + ' is not "c,r"'); continue; }
      if (!free(i, j)) bad.push('crawl ' + k + ' not walkable');
      else if (K([i, j]) !== K(start) && !findPath(start, [i, j], new Set(), WORKS)) bad.push('crawl ' + k + ' unreachable for Works crew');
    }
  }
  return { bad, tiers, win, crawl: crawl.length };
})()"""

# Pillar 5 Step 4 (0.53.4, R4's ask): a deck's leak joints (DECKS[n].leakJoints, M13): each one's place stands on a free tile,
# its wall edge is a real wall or a straight hull (not a door, glass or open floor), and its puddle place is free and in the room
LEAKS = r"""(() => { const L = deckDef.leakJoints; if (!L) return null;
  const key = (c, r, f) => ({ n: `h,${c},${r}`, s: `h,${c},${r + 1}`, w: `v,${c},${r}`, e: `v,${c + 1},${r}` })[f], bad = [];
  for (const j of L) { const p = PLACE_OF.get(j.place), q = PLACE_OF.get(j.puddlePlace);
    if (!p) { bad.push(j.place + ': no place'); continue; }
    const e = EDGES.get(key(p.at[0], p.at[1], j.wall));
    if (BLOCKED.has(K(p.at))) bad.push(j.place + ': its tile is blocked');
    if (!e || !['wall', 'hull'].includes(e.type)) bad.push(j.place + ': its wall edge is ' + (e ? e.type : 'open floor'));
    if (j.puddlePlace && (!q || BLOCKED.has(K(q.at)) || q.room !== p.room)) bad.push(j.puddlePlace + ': the puddle\'s place is missing, blocked or in another room'); }
  return { n: L.length, bad }; })()"""

# 0.92.5 (the user's item 7, "booths and sofas in the lounge clip and flicker"): in each seat kit, no two of its boxes share an
# outer face (the same plane, the same side, overlapping): the phones-first rule, no coplanar surfaces
COPLANAR = r"""(kinds => { const out = {};
  for (const [kind, o] of kinds) { const g = new THREE.Group(); KIT[kind](g, o); g.updateMatrixWorld(true); const bx = [];
    g.traverse(m => { if (!m.isMesh || !m.geometry || m.geometry.type !== 'BoxGeometry' || m.material === HIT_MAT) return;
      const e = m.rotation; if (Math.abs(e.x) + Math.abs(e.y) + Math.abs(e.z) > 1e-6 || m.parent !== g) return;   // axis-aligned boxes only
      m.geometry.computeBoundingBox(); const b = m.geometry.boundingBox.clone().applyMatrix4(m.matrixWorld); bx.push(b); });
    const bad = [], E = 1e-4, A = ['x', 'y', 'z'];
    for (let i = 0; i < bx.length; i++) for (let j = i + 1; j < bx.length; j++) for (let a = 0; a < 3; a++) for (const s of ['min', 'max']) {
      if (Math.abs(bx[i][s][A[a]] - bx[j][s][A[a]]) > E) continue;   // the same face plane, the same side
      const [p, q] = A.filter((_, k) => k !== a), ov = (Math.min(bx[i].max[p], bx[j].max[p]) - Math.max(bx[i].min[p], bx[j].min[p])) * (Math.min(bx[i].max[q], bx[j].max[q]) - Math.max(bx[i].min[q], bx[j].min[q]));
      if (Math.min(bx[i].max[p], bx[j].max[p]) - Math.max(bx[i].min[p], bx[j].min[p]) > E && Math.min(bx[i].max[q], bx[j].max[q]) - Math.max(bx[i].min[q], bx[j].min[q]) > E) bad.push(i + '/' + j + ' ' + s + A[a] + ' ' + ov.toFixed(4)); }
    out[kind + (o.w ? ' w ' + o.w : '')] = bad; }
  return out; })"""
SEAT_KITS = "[['booth', {}], ['sofa', { w: 2.4 }], ['sofa', { w: 2.0 }], ['armchair', {}], ['windowSeat', {}], ['beanbag', {}]]"

with sync_playwright() as pw:
    g = Game(pw, sys.argv[1])
    cp = g.ev(f"({COPLANAR})({SEAT_KITS})")
    print('Seat kits, faces shared between their boxes (none wanted):', cp)
    if any(cp.values()): ok_seats = False; print('  a seat kit has coplanar faces (they flicker)')
    else: ok_seats = True
    decks = g.ev("typeof DECK_ORDER !== 'undefined' ? DECK_ORDER.slice().sort((a, b) => a - b) : Object.keys(DECKS).map(Number)")
    ok = ok_seats
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
        lk = g.ev(LEAKS)
        if lk is not None:
            print(f"  leak joints: {lk['n']}")
            if lk['bad']: print(f"  bad leak joints: {lk['bad']}"); ok = False
        tg = g.ev(TAGS)
        if tg['tiers'] or tg['win'] or tg['crawl']:
            print(f"  tags: service tiers {tg['tiers']}, window places {tg['win']}, crawl tiles {tg['crawl']}")
        if tg['bad']:
            print(f"  bad tags ({len(tg['bad'])}): {tg['bad'][:12]}"); ok = False
    mem = []
    for n in [d for d in decks if d != 4] * 3:
        g.ev(f"goToDeck({n})"); g.step(3); g.ev("goToDeck(4)"); g.step(3)
        mem.append(g.ev("JSON.stringify([renderer.info.memory, DECK_CREW.filter(a => a.h.full).map(a => a.p.id).sort()])"))
    print('Deck 4 memory after round trips (and the story crew near you with a full body):', mem)
    # story crew near you get a full body (crewDetail), freed when they go: compare trips with the same ones (0.71.4)
    same = {}
    for m in mem[len(decks) - 1:]: v = json.loads(m); same.setdefault(','.join(v[1]), set()).add(json.dumps(v[0]))
    if any(len(v) > 1 for v in same.values()): ok = False; print('  memory changes between round trips')
    if not any(sum(1 for m in mem[len(decks) - 1:] if ','.join(json.loads(m)[1]) == k) > 1 for k in same): ok = False; print('  no two round trips to compare')
    # 0.92.5 (the user's item 6): the auditorium's piano (and its bench) is on stage only during talent night, tappable only then
    if 7 in decks:
        g.ev("goToDeck(7)"); g.step(3)
        td = g.ev("(() => { for (let d = 1; d <= 60; d++) if (tradOn('rec-talent-night', (d - 1) * 1440 + 1180)) return d; return null; })()")
        pn = []
        for m in ([1080, 1180, 1300] if td else []):
            g.ev(f"setShipNow(({td} - 1) * 1440 + {m})"); g.step(30)
            pn.append(g.ev("(() => { const it = ITEMS.find(i => i.t === 'Grand piano'); return [REC_SHOW.state, (REC_SHOW.piano || []).map(q => q.visible).concat(!!it && isShown(it.hit))]; })()"))
        print(f"  the auditorium piano on talent night (Day {td}) at 18:00, 19:40, 21:40: [show, piano, bench, tappable]", pn)
        if pn != [[None, [False, False, False]], ['talent', [True, True, True]], [None, [False, False, False]]]: ok = False; print('  the piano should be on stage (and tappable) only during talent night')
    print('errors', g.errors)
    if g.errors: ok = False
    g.close()
    # the comet (FX25, 0.93.2; plans/events-plan-2.html A8): draw calls at a phone's size (390 x 844) with the comet's crowd
    # settled, the sky shape up and the dressing out: the bow lounge at 21:45 (about 30-45 at the glass) and the junior
    # common room at 22:20 (the blankets, the tail); each under the 450 budget, the sky shape one draw call of its own
    g = Game(pw, sys.argv[1], 390, 844)
    if g.ev("typeof EV_COMET_ON !== 'undefined' && EV_COMET_ON && !!SHIP_EVENTS.comet"):
        g.ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }")
        g.ev("skipTo(21 * 1440 + 1260)")
        for name, deck, room, m in (('the bow lounge, 21:45', 3, 'L', 1305), ('the junior common room, 22:20', 4, 'j', 1340)):
            g.ev(f"for (let t = Math.max(shipNow() + 1, 21 * 1440 + {m - 6}); t <= 21 * 1440 + {m}; t++) {{ setShipNow(t); EV_MIN = -1; eventsTick(); }}")
            g.ev(f"(() => {{ goToDeck({deck}); deckCrewFill(); const tl = ROOM_TILES['{room}'], c = cellPos(...tl[Math.floor(tl.length / 2)]); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); target.copy(player.obj.position).setY(.7); eventsDress(shipNow()); }})()")
            g.step(40)
            c = g.ev("({ calls: renderer.info.render.calls, crew: DECK_CREW.filter(a => a.settled && a.spot && a.spot.room === roomAt(...player.here())).length, sky: !!COMET_SKY.m, dress: [...DRESS.on.keys()].filter(k => /^comet/.test(k)) })")
            g.ev("COMET_SKY.m.visible = false"); g.step(1); c['noSky'] = g.ev("renderer.info.render.calls"); g.ev("COMET_SKY.m.visible = true")
            print(f"The comet, {name}, phone size: draw calls {c['calls']} ({c['noSky']} without the sky shape), {c['crew']} settled in the room, the sky shape {c['sky']}, dressing {c['dress']}")
            if c['calls'] >= 450 or not c['sky'] or c['calls'] - c['noSky'] > 1 or c['crew'] < 6: ok = False; print('  the comet scene: over budget, no sky shape, more than one call for it, or nobody there')
        if g.errors: ok = False; print('errors (the comet)', g.errors[:4])
    else: print('The comet: switched off')
    g.close()
    # A Veyli vessel needs help (VB2: V-5 and V-3's spots, plans/veyli-vessel-spec.html), on a copy with EV_VESSEL_ON on (a
    # preview switch until its switch-on turn; added to the copy when the build hasn't the line yet): the parts chain's 40
    # spots and Zeke's on Deck 5 pass the places check, in line order, each within a tile of the next; and, once VB1's
    # event is in, draw calls at a phone's size in the Works bay during the chain (the props, the crates) and at the bow
    # glass at 17:41 Monday (the ship outside lit), each under the 450 budget, the ship one draw call of its own
    src = open(sys.argv[1]).read()
    if not re.search(r'const EV_VESSEL_ON = true\b', src):
        src = re.sub(r'const EV_VESSEL_ON = [^;]+;', 'const EV_VESSEL_ON = true;', src, count=1) if 'const EV_VESSEL_ON' in src else src.replace('const P926_APPT = ', 'const EV_VESSEL_ON = true;\nconst P926_APPT = ', 1)
    vp = WORK / 'test' / ('_vessel_' + os.path.basename(sys.argv[1])); vp.write_text(src)
    g = Game(pw, str(vp), 390, 844)
    if g.ev("typeof vesselOn === 'function' && vesselOn()"):
        g.ev("if (typeof GUIDE_ON !== 'undefined' && GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }")
        g.ev("goToDeck(5)"); g.step(3)
        pl = g.ev(PLACES)
        vc = g.ev("(() => { const V = DECKS[5].vesselChain, ps = V.spots.map(id => deckDef.places.find(p => p.id === id)); return { n: ps.filter(Boolean).length, call: !!deckDef.places.find(p => p.id === V.call), you: V.spots.includes(V.you), gap: Math.max(...ps.slice(1).map((p, k) => Math.hypot(p.xy[0] - ps[k].xy[0], p.xy[1] - ps[k].xy[1]))) }; })()")
        bad = [b for b in pl['bad'] if re.match(r'5-v(chain|bench|shop)', b)]
        nb = g.ev("deckDef.places.filter(p => /^5-v(bench|shop)-/.test(p.id)).length")
        print(f"The Veyli vessel: the bench spots (Works bay and machine shop): {nb} (want 6)")
        if nb != 6: ok = False
        print(f"The Veyli vessel: the chain's spots on Deck 5: {vc['n']} (Zeke's {vc['call']}, yours in the line {vc['you']}), the widest gap {vc['gap']:.2f} tiles; bad: {bad}")
        if vc['n'] != 40 or not vc['call'] or not vc['you'] or vc['gap'] > 1.0 or bad: ok = False; print('  the chain spots: not 40, a spot missing, a gap over a tile, or a bad place')
        if g.ev("!!SHIP_EVENTS.veyliVessel"):
            g.ev("skipTo(27 * 1440 + 780); if (!SHIP.event || SHIP.event.id !== 'veyliVessel') eventStart('veyliVessel', 27)")
            for name, deck, room, day, m in (('the parts chain, Works bay, Sunday 13:30', 5, 'w', 28, 810), ('the engine lights, the bow lounge, Monday 17:41', 3, 'L', 29, 1061)):
                g.ev(f"for (let t = Math.max(shipNow() + 1, {day - 1} * 1440 + {m - 6}); t <= {day - 1} * 1440 + {m}; t++) {{ setShipNow(t); EV_MIN = -1; eventsTick(); }}")
                # the Works bay: its middle; the bow lounge: its bow-most open tile, at the glass (RV21's should 3: the ship on screen from there)
                g.ev(f"(() => {{ goToDeck({deck}); deckCrewFill(); const tl = ROOM_TILES['{room}'], bow = {str(deck == 3).lower()} ? tl.filter(([i, j]) => free(i, j)).sort((a, b) => b[0] - a[0] || Math.abs(a[1] - 11) - Math.abs(b[1] - 11))[0] : null, c = cellPos(...(bow || tl[Math.floor(tl.length / 2)])); player.obj.position.copy(cellPos(...nearestOpen(c.x, c.z, player))); player.stop(); target.copy(player.obj.position).setY(.7); eventsDress(shipNow()); }})()")
                g.step(40)
                c = g.ev("({ calls: renderer.info.render.calls, crew: DECK_CREW.length, sky: !!VSKY.m, dress: [...DRESS.on.keys()].filter(k => /^vessel/.test(k)), onScreen: !!VSKY.m && (p => p.x >= 0 && p.x <= innerWidth && p.y >= 0 && p.y <= innerHeight)(VSKY.m.material.uniforms.uP.value) })")
                if c['sky']: g.ev("VSKY.m.visible = false"); g.step(1); c['noSky'] = g.ev("renderer.info.render.calls"); g.ev("VSKY.m.visible = true")
                else: c['noSky'] = c['calls']
                print(f"The Veyli vessel, {name}, phone size: draw calls {c['calls']} ({c['noSky']} without the ship outside), {c['crew']} on the deck, the ship outside {c['sky']} (on screen {c['onScreen']}), dressing {c['dress']}")
                if c['calls'] >= 450 or c['calls'] - c['noSky'] > 1 or (deck == 3 and not (c['sky'] and c['onScreen'])): ok = False; print('  the vessel scene: over budget, no ship outside on screen at the glass, or more than one call for it')
        else: print("The Veyli vessel: its event isn't in this build yet (VB1's block): the scenes wait")
        if g.errors: ok = False; print('errors (the Veyli vessel)', g.errors[:4])
    else: print('The Veyli vessel: not in this build')
    g.close(); vp.unlink(missing_ok=True)
    print('DECK CHECK OK' if ok else 'DECK CHECK FAILED')
    sys.exit(0 if ok else 1)   # so a failing check fails for the computer too (check_fast.sh, GitHub)
