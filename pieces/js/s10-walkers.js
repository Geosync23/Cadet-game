// =====================================================================
// 10. WALKERS
// Movement shared by you and the crew: paths on the tile grid, gentle
// steering, simple yielding when someone is in the way, and the gait.
// =====================================================================
// the deck you start on: built before anyone is placed on it (Deck 4, or the save's: section 13)
buildDeck(DECKS[START.deck]); indexRoomTiles();

const walkers = [];
const DECK_CREW = [];                                    // the scheduled crew on this deck (CrewAgent, below)
const cellAt = (x, z) => [Math.floor(x + OX), Math.floor(z + OZ)];
const K = c => c[0] + ',' + c[1];
function occupiedBy(except) {                 // cells other people stand in, or are heading to
  const s = new Set();
  for (const o of walkers) if (o !== except && o.active) { s.add(K(o.here())); if (o.goal) s.add(K(o.goal)); }
  for (const a of DECK_CREW) if (a.settled && a.spot && a.spot.onTile) s.add(K(a.spot.walk));   // crew standing at their place
  return s;
}
function nearestOpen(x, z, who) {
  const taken = occupiedBy(who); let best = null, bd2 = 1e9;
  for (let a = 0; a < W; a++) for (let b = 0; b < D; b++) {
    if (!free(a, b) || taken.has(a + ',' + b)) continue;
    const p = cellPos(a, b), d = (p.x - x) ** 2 + (p.z - z) ** 2;
    if (d < bd2) { bd2 = d; best = [a, b]; }
  }
  return best;
}
class Walker {
  constructor(spec, cell, isPlayer = false) {
    this.id = walkers.length; this.spec = spec; this.isPlayer = isPlayer; this.active = true;
    this.rig = makeCharacter(spec); this.h = this.rig.spec.height;
    this.obj = new THREE.Group(); this.obj.add(this.rig.root); scene.add(this.obj);
    this.obj.traverse(o => { o.userData.walker = this; });
    this.deck = spec.deck;
    if (this.deck === deckDef.num) {
      if (!free(...cell)) { const p = cellPos(...cell); cell = nearestOpen(p.x, p.z, this) || cell; }
      this.obj.position.copy(cellPos(...cell));
    } else { this.active = false; this.obj.visible = false; }   // off on another deck until you go there
    this.spawn = cell;
    this.obj.rotation.y = isPlayer ? Math.PI : R() * 6.28; this.face = this.obj.rotation.y;
    this.g = { p: 0, w: 0, turn: 0, look: 0, lookT: R() * 3, tail: 0, tailV: 0, lean: 0, t0: R() * 20 };
    this.path = []; this.goal = null; this.vel = 0; this.onArrive = null;
    this.stuck = 0; this.rest = .5 + R() * 4; this.talking = 0; this.maxV = 1.2 * Math.sqrt(this.h) * (spec.speed || 1);
    walkers.push(this);
  }
  here() { return cellAt(this.obj.position.x, this.obj.position.z); }
  goTo(goal, cb, extraAvoid) {
    const avoid = occupiedBy(this); if (extraAvoid) avoid.add(K(extraAvoid));
    // your goal on a tile two places share (the cook's station on a range panel): the crew member there makes way, so
    // it's yours unless another walker is on it or heading for it. Passing through, you still squeeze past (0.26.37)
    if (this.isPlayer && goal && sharedTile(goal) && !walkers.some(o => o !== this && o.active && (K(o.here()) === K(goal) || o.goal && K(o.goal) === K(goal)))) avoid.delete(K(goal));
    if (!goal || !free(...goal) || avoid.has(K(goal))) return false;
    let p = findPath(this.here(), goal, avoid, this);
    if (!p && this.isPlayer && typeof squeezePath === 'function') p = squeezePath(this, goal, avoid);   // section 15: squeeze past settled crew
    if (!p) return false;
    this.path = p.length ? p : [goal]; this.goal = goal; this.onArrive = cb || null;
    return true;
  }
  stop() { this.path = []; this.goal = null; this.onArrive = null; }
  faceToward(o) { this.face = Math.atan2(o.obj.position.x - this.obj.position.x, o.obj.position.z - this.obj.position.z); }
  update(dt, t) {
    const pos = this.obj.position; let moved = 0;
    if (this.steer) {                                    // press-and-hold: walk where the finger points
      const s = this.steer, ox = pos.x, oz = pos.z;
      this.vel += (this.maxV * s.k - this.vel) * Math.min(1, dt * 5);
      pos.x += s.x * this.vel * dt; pos.z += s.z * this.vel * dt;
      for (const o of walkers) {                         // don't walk through people
        if (o === this || !o.active) continue;
        if (this.isPlayer && typeof pushThrough === 'function' && pushThrough(o, o.obj.position.x, o.obj.position.z, pos)) continue;   // section 15 (playtest 1)
        const qx = pos.x - o.obj.position.x, qz = pos.z - o.obj.position.z, qd = Math.hypot(qx, qz);
        if (qd < .42 && qd > 1e-4) { pos.x = o.obj.position.x + qx / qd * .42; pos.z = o.obj.position.z + qz / qd * .42; }
      }
      for (const a of DECK_CREW) {                       // nor through crew on their feet
        const bp = a.settled && a.spot ? a.spot.pose : a.pose; if (bp === 'sit' || bp === 'lie') continue;
        if (this.isPlayer && typeof shuffleable === 'function' && shuffleable(a)) continue;   // section 15: on their feet and not at a place, they step aside for you (0.28.70)
        if (this.isPlayer && typeof pushThrough === 'function' && pushThrough(a, a.x, a.z, pos)) continue;   // section 15: pushing 2 s, you get by (playtest 1)
        const qx = pos.x - a.x, qz = pos.z - a.z, qd = Math.hypot(qx, qz);
        if (qd < .42 && qd > 1e-4) { pos.x = a.x + qx / qd * .42; pos.z = a.z + qz / qd * .42; }
      }
      collide(pos, BODY_R, this);
      moved = Math.hypot(pos.x - ox, pos.z - oz);
      if (s.k > .02) this.face = Math.atan2(s.x, s.z);
    } else if (this.path.length) {
      const last = this.path.length === 1, p = cellPos(...this.path[0]);
      const dx = p.x - pos.x, dz = p.z - pos.z, d = Math.hypot(dx, dz) || 1e-6;
      // anyone in the way? lower id has right of way; standing people are walked around
      let block = null;
      for (const o of walkers) {
        if (o === this || !o.active) continue;
        const ox = o.obj.position.x - pos.x, oz = o.obj.position.z - pos.z, od = Math.hypot(ox, oz);
        if (od < .62 && (ox * dx + oz * dz) / (od * d + 1e-6) > .35 && (!o.path.length || o.id < this.id)) { block = o; break; }
      }
      if (block) {
        this.vel *= Math.max(0, 1 - dt * 10); this.stuck += dt;
        if (!block.path.length || this.stuck > .9) {
          this.stuck = 0; const g = this.goal, cb = this.onArrive;
          if (!(g && this.goTo(g, cb, block.here()))) this.stop();
        }
      } else {
        this.stuck = 0;
        const want = last ? Math.min(this.maxV, .3 + d * 2.2) : this.maxV;
        this.vel += (want - this.vel) * Math.min(1, dt * 4);
        const step = this.vel * dt;
        if (last && d <= Math.max(step, .01)) {
          pos.x = p.x; pos.z = p.z; moved = d; this.path.shift(); this.goal = null;
          const cb = this.onArrive; this.onArrive = null; if (cb) cb();
        } else {
          if (!last && d < .25) this.path.shift();          // small corner cut; keeps clear of door frames
          const st = Math.min(step, d); pos.x += dx / d * st; pos.z += dz / d * st; moved = st;
          this.face = Math.atan2(dx, dz);
        }
      }
    } else this.vel = 0;
    if (this.press) {                                    // reaching for a button: up, a tap, back down
      const pr = this.press; pr.t += dt;
      if (moved > 0) this.press = null;
      else {
        if (!pr.fired && pr.t >= .42) { pr.fired = true; if (pr.cb) pr.cb(); }
        if (pr.t >= .8) this.press = null;
      }
    }
    this.g.reach = this.press ? (this.press.t < .3 ? ss(this.press.t / .3) : this.press.t < .5 ? 1 : 1 - ss((this.press.t - .5) / .3)) : 0;
    const prev = this.obj.rotation.y;
    let df = this.face - prev; df = Math.atan2(Math.sin(df), Math.cos(df));
    this.obj.rotation.y += df * Math.min(1, dt * 8);
    const g = this.g;
    g.turn += ((this.obj.rotation.y - prev) / Math.max(dt, 1e-3) - g.turn) * Math.min(1, dt * 10);
    g.p += moved / (CYCLE * this.h);
    if (!moved && g.w < .02) g.p = 0;
    g.w += ((moved > 0 ? 1 : 0) - g.w) * Math.min(1, dt * (moved > 0 ? 6 : 7));
    if (this.towel !== undefined && this.towel !== null && shipNow() >= this.towel) this.towel = null;   // 0.81.0: the towel after a swim (recTowel)
    if (this.holding !== undefined || this.crouch !== undefined || this.deviceOut !== undefined || this.needGo !== undefined || this.towel !== undefined) animateActivity(this, (this.crouch ? 'crouch' : 'stand') + (this.holding ? '+' + (this.holding === true ? 'carry' : this.holding) : this.deviceOut ? '+device' : this.needGo ? '+go' : this.towel ? '+towel' : ''), dt, t + g.t0, Math.min(1, this.vel / this.maxV));   // section 15: in hand (8b's '+carry', '+cart', '+cartfull'), crouching in a crawlway
    else animateRig(this.rig, g, dt, t + g.t0, Math.min(1, this.vel / this.maxV));
  }
  setActive(on) {
    this.active = on; this.obj.visible = on; this.stop();
    if (on) { const p = cellPos(...this.spawn), c = nearestOpen(p.x, p.z, this); if (c) this.obj.position.copy(cellPos(...c)); this.rest = R() * 2; }
  }
}

const player = new Walker({ ...PLAYER_SPEC, deck: START.deck }, START.tile || PLAYER_SPEC.start, true);
if (START.face != null) player.face = player.obj.rotation.y = START.face;
// The nine placeholder walkers are gone (0.22.1): the crew are the scheduled CrewAgents now. CREW (section 9)
// stays as data; `crew` stays, empty, for the code that still loops over it.
const crew = [];
target.copy(player.obj.position).setY(.7);

// ---- the crew on this deck (Pillar 1, workstream 6) ----
// Everyone whereIs (section 14) puts on the deck you're on is a CrewAgent here: they walk the tile grid to their
// place, settle into its pose (sit, stand, lie, work), and walk on when their schedule moves them. They are drawn
// by the crowd (section 8b). When you arrive on a deck they're already mid-activity: at their place, or partway
// there if they set off only a little while ago. They arrive and leave by the lift car. A 'closed' door is open
// to someone whose own bed, or whose destination, is in the room behind it (crewPath). After a time skip (sleep)
// everyone is placed afresh. Crew don't block each other; you can't walk through anyone standing still.
// Nothing here calls R(): any choice comes from the person's id.
const CREW_SPEED = 1.15;                                 // tiles per real second
const _cp = new THREE.Vector3();
const FACE_ANGLE = { s: 0, n: Math.PI, e: Math.PI / 2, w: -Math.PI / 2 };
// seat and mattress tops (the performance engineer's measurements): a place's own `y` wins, then beds (upper
// berths, the even ones, at 1.6), then these by type; 0 is the crowd's default (0.475 to sit, 0.5 to lie)
const SEAT_Y = { 'mess-seat': .475, bench: .48, 'lounge-seat': .44, 'common-room': .44 };
const idHash = s => { let h = 7; for (let i = 0; i < s.length; i++) h = Math.imul(h ^ s.charCodeAt(i), 16777619); return h >>> 0; };
let SPOT_OF = new Map(), PLACE_OF = new Map();          // this deck's places, and where each one is (made per deck)
const edgeTiles = k => { const [o, i, j] = k.split(','); return o === 'v' ? [[+i - 1, +j], [+i, +j]] : [[+i, +j - 1], [+i, +j]]; };
// where a place is: the tile to walk to, the exact spot, the height (an upper bunk is high), the pose and facing
function placeSpot(id) {
  if (SPOT_OF.has(id)) return SPOT_OF.get(id);
  const pl = PLACE_OF.get(id); let s = null;
  if (!pl && id[0] === '@') s = lineSpotMake(id);       // the servery line past its queue places
  else if (pl) {
    const c = cellPos(...pl.at); let x = pl.xy ? pl.xy[0] - OX : c.x, z = pl.xy ? pl.xy[1] - OZ : c.z;
    if (pl.type === 'bed' && !pl.xy) {                   // a bed is longer than a tile: lie on the middle of the bed itself
      let best = null, bd = 1.3;
      for (const it of ITEMS) if (/bunk|bed|futon/i.test(it.t)) { it.hit.getWorldPosition(_cp); const d = Math.hypot(_cp.x - c.x, _cp.z - c.z); if (d < bd) { bd = d; best = [_cp.x, _cp.z]; } }
      if (best) [x, z] = best;
    }
    let walk = pl.walk || (free(...pl.at) ? pl.at : null);
    if (!walk) {                                         // a seat or bed: the open tile beside it in its room, nearest the spot
      const [a, b] = pl.at, opts = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]].map(([di, dj]) => [a + di, b + dj])
        .filter(n => free(...n) && roomAt(...n) === pl.room && (n[0] === a || n[1] === b ? edgeOpen(a, b, ...n) : true))   // never through a wall
        .sort((m, n) => cellPos(...m).distanceTo(new THREE.Vector3(x, 0, z)) - cellPos(...n).distanceTo(new THREE.Vector3(x, 0, z)));
      const lift = liftTiles()[0], rooms = new Set([pl.room]);   // the nearest one you can actually get to from the lift
      const who = /^work:works/.test(pl.type) ? { dept: 'works' } : undefined;   // a Works place behind a service hatch
      walk = opts.find(n => !lift || K(n) === K(lift) || crewPath(lift, n, rooms, who)) || opts[0] || nearestOpen(x, z, null);
    }
    const berth = pl.type === 'bed' && /^4-B\d+-(\d+)$/.exec(id);
    const y = pl.y !== undefined ? pl.y : pl.type === 'bed' ? (berth && +berth[1] % 2 === 0 ? 1.6 : .5) : SEAT_Y[pl.type] || 0;
    // facing: a compass letter, or a number in degrees (round tables, the curved bar, card tables; 0 = south, 90 = east,
    // as the letters); a place's own `y` (seat height) always wins over SEAT_Y, for the crew and the player alike
    s = { id, walk, x, z, y, face: typeof pl.face === 'number' ? pl.face * Math.PI / 180 : FACE_ANGLE[pl.face] || 0,
      pose: pl.type === 'bed' ? 'lie' : pl.pose, anim: placeAnim(pl), room: pl.room, onTile: free(...pl.at), mv: pl.move || null };   // mv: 8c's crew moves (0.84.6)
  }
  SPOT_OF.set(id, s); return s;
}
// the pose at a place: its activity (run, lift, call, play...) once the crowd can show it (section 8b lists those in
// CROWD_ANIMS), else the place's plain pose, so a seated pianist stays seated until 'play' exists
// (the activity comes from the plan's segment, which knows the task: tea on the galley stool is the stool's own pose)
// The pose string the crowd takes (8b): 'base:activity' when seated or lying ('sit:play', 'lie:lift'), the
// activity alone when standing ('browse', 'run'), else the plain pose. What the plan says they're doing comes first
// (TAG_ACT: a musician plays, a bar regular drinks, the dish pit washes, tea on the galley stool just sits); then
// someone sitting about in a lounge, common room or on a bench reads, talks or has a drink (seeded per person, place
// and day); then the place itself (poseOf, 8b). Collisions and taps use the place's plain pose (spot.pose).
const TAG_ACT = { play: 'play', bar: 'drink', wash: 'wash', tea: null, handover: 'talk', stroll: null };
const SIT_ABOUT = new Set(['lounge-seat', 'common-room', 'bench']);
// the pose with what's held: '+cart', '+cartfull' or '+carry' after it (the crowd's held things, 8b)
const heldPose = a => a.hold ? a.pose + '+' + a.hold : a.pose;
// crew hobbies (0.36.89, plan-0607): crewHobby(p) -> one of the player's seven hobby ids (section 15's HOBBIES: read,
// write, games, draw, knit, puzzle, stars) from the roster's hobby words, else null. Seated in their free time at a
// common seat, someone with a hobby in hand does it most of the time (the 'read' activity: the crowd has no knitting
// or drawing of its own yet); a stargazer on a window seat just looks out. Pure: no R(), no state
const HOBBY_WORDS = [['knit', /knit|crochet/], ['draw', /draw|sketch|paint|comic/], ['puzzle', /crossword|puzzle|card trick|knot|sudoku/], ['write', /writ|journal|letter|poem|diary/],
  ['read', /read|novel|book/], ['games', /\btiles\b|chess|game/], ['stars', /star|telescope|constellation|sky/]];
function crewHobby(p) {
  const h = String(p && (p.hobby || p.hobbyNoun) || '').toLowerCase(); if (!h) return null;
  for (const [id, re] of HOBBY_WORDS) if (re.test(h)) return id;
  return null;
}
function crewPose(a) {
  const sp = a.spot, pl = PLACE_OF.get(sp.id), base = sp.pose;
  if (typeof CROWD_ANIMS === 'undefined') return base;
  const ok = x => x && CROWD_ANIMS.has(x), comp = x => base === 'sit' || base === 'lie' ? base + ':' + x : base === 'stand' || base === 'work' ? x : base;
  if (a.tag in TAG_ACT) { const x = TAG_ACT[a.tag]; return ok(x) ? comp(x) : base; }
  if (base === 'sit' && pl && SIT_ABOUT.has(pl.type) && !pl.anim) {
    const u = idHash(a.p.id + '|' + sp.id + '|' + SHIP.time.day) % 100, hb = crewHobby(a.p);
    if (hb === 'stars' && pl.window) return base;         // a stargazer at the window: just looking out
    const x = u < (hb && hb !== 'stars' ? 75 : 45) ? 'read' : u < 80 || pl.type !== 'lounge-seat' ? 'talk' : 'drink';   // a hobby in hand: at it three times in four
    if (ok(x)) return 'sit:' + x;
  }
  return typeof poseOf === 'function' && pl ? poseOf(pl) : base;
}
// findPath, with the 'closed' doors into `rooms` open for the moment; `who` (a CrewAgent or roster person) is passed
// on so service hatches open for Works crew (hatchPassable, section 4)
function crewPath(s, g, rooms, who, avoid) {
  const opened = [];
  for (const k in CLOSED_DOORS) {
    const e = EDGES.get(k);
    if (e && e.type === 'closed' && edgeTiles(k).some(c => rooms.has(roomAt(...c)))) { e.type = 'door'; opened.push(e); }
  }
  try { return findPath(s, g, avoid, who); } finally { for (const e of opened) e.type = 'closed'; }
}
// The servery line on Deck 3 (0.26.30): LINE is who's standing in it, front first (crew ids, and 'player' when
// section 15 joins you): real bodies only, joined on reaching its back. Its spots run up column 33 from the counter
// (3-queue-4, at the servery's south end) past the trays (3-queue-1), then back along the row-2 aisle; past those,
// stand where you are. The first LINE_COUNTER stand along the servery and are served there after galleyServeMins
// (section 16; LINE_SERVE until then) when galleyCanServe says there's food; you're served by section 15, which
// calls lineLeave('player'). No tray return (0.36.85, the user's): a diner's tray goes away when the meal is over.
// For other sections: servLine() (who's in it, front first), lineJoin(id), lineLeave(id), lineSpot(id) ({ at, xy,
// face } to stand at, null past the spots), lineFront(id) (at the servery). LINE_LOG counts for day_check.
const LINE_AT = [[33, 6], [33, 5], [33, 4], [33, 3], [32, 3], [32, 2], [31, 2], [30, 2], [29, 2], [28, 2], [27, 2], [26, 2], [25, 2], [24, 2], [23, 2]];
const LINE_Q = ['3-queue-4', '3-queue-3', '3-queue-2', '3-queue-1'];   // the queue places, front first
const LINE_SERVE = .6, LINE_LATE = 12;
// how many are served at once: one, or two while a meal tradition is on (the galley's second server: 0.26.41)
let LINE_COUNTER = 1, LINE_CMIN = -1;
function lineCounter(now) {
  const m = Math.floor(now); if (m === LINE_CMIN) return LINE_COUNTER; LINE_CMIN = m;
  const d = Math.floor(m / 1440) + 1, t = m - (d - 1) * 1440;
  LINE_COUNTER = typeof eventsOn === 'function' && eventsOn(d).some(e => e.ev.meal && t >= e.from - TRAD_LINE[1] - 5 && t < e.to) ? 2 : 1;
  return LINE_COUNTER;
}                   // ship minutes: serving one at the counter, still heading for the line after the meal's time; how many are served at once
const LINE = [], LINE_LOG = { joined: 0, served: 0, trays: 0, left: 0, returned: 0, long: 0, wait: 0, who: [] };   // returned: trays gone with the meal over
const lineSpotId = k => k < LINE_Q.length ? LINE_Q[k] : k < LINE_AT.length ? '@line-' + k : null;
const ALT_SEAT = new Set(['mess-seat', 'lounge-seat', 'bench']);   // places where someone sitting in yours sends you to the next one
let MESS_ONLY = null;                                    // Deck 3's tiles outside the mess hall, for findPath's avoid (made once a deck)
const messOnly = () => { if (!MESS_ONLY || MESS_ONLY.d !== deckDef) { MESS_ONLY = new Set(); MESS_ONLY.d = deckDef; for (const r in ROOM_TILES) if (r !== 'M') for (const t of ROOM_TILES[r]) MESS_ONLY.add(t[0] + ',' + t[1]); } return MESS_ONLY; };
const lineSeg = w => w.type === 'servery-queue' || w.tag === 'queue';   // the plan's walk to the line, its queue stop, a grab at the servery
const trayTo = id => { const pl = id && PLACE_OF.get(id); return !!pl && pl.room === 'M'; };   // a tray only to a seat in the mess hall
// the shower queue's stand-in spots (0.36.91): open tiles of the washroom beside its way out, '@wq-<room>-<k>'
let WQ_TILES = null;
function washDoorTiles(rk) {
  if (!WQ_TILES || WQ_TILES.d !== deckDef) { WQ_TILES = new Map(); WQ_TILES.d = deckDef; }
  if (!WQ_TILES.has(rk)) {
    const used = new Set((deckDef.places || []).map(q => placeSpot(q.id)).filter(Boolean).map(sp => sp.walk && sp.walk.join(',')));
    const T = ROOM_TILES[rk] || [], door = T.filter(([i, j]) => [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([a, b]) => free(i + a, j + b) && roomAt(i + a, j + b) !== rk && edgeOpen(i, j, i + a, j + b)));
    const dd = ([i, j]) => Math.min(...door.map(([x, y]) => Math.abs(x - i) + Math.abs(y - j))), open = T.filter(([i, j]) => !used.has(i + ',' + j));
    const m = door.length && open.length ? Math.min(...open.map(dd)) : 0;
    WQ_TILES.set(rk, door.length ? open.filter(t => dd(t) <= Math.max(m, 0)) : []);   // the free tiles by the way out (beside it, when a basin's walk-to tile has the doorway itself)
  }
  return WQ_TILES.get(rk);
}
function showerQSpot(a, w) {
  const nx = whereIs(a.p, w.until), pl = nx && nx.placeId && PLACE_OF.get(nx.placeId); if (!pl) return null;
  const l = washDoorTiles(pl.room); return l.length ? '@wq-' + pl.room + '-' + (idHash(a.p.id) % l.length) : null;
}
// the live queues at the call booths and the showers (0.71.4, the user's playtest 2 items 15 + 20: "a queue at the
// booths, with a message saying your place in line", "a visible queue at the showers"): whoever's plan has them
// waiting for one (tag 'boothq', 'showerq'), or heading for the one you're using, stands in a line in that room in the
// order they came into the room (on the way, they head for the back); you join at the back (queueJoin, from section 15's tap on a busy booth or shower) and take
// the first free one once nobody's ahead of you. While you wait, anyone who came after you waits behind you. Live only,
// not saved (as the servery line): a load starts you out of it. The line: the deck architect's 'shower-queue' places,
// then open tiles of the room leading away from them (or from the middle of the booths), past every place's tile and
// the doorways. For other sections: queueOf(type) ('callhome' or 'shower') -> { ids: front first ('player' is you), you }
const QUEUE_TAGS = { boothq: 'callhome', showerq: 'shower' }, QUEUE_MAX = 6;
const QUEUE_NOW = new Map(), QUEUE_SPOT = new Map(), QUEUE_IN = new Map(), QUEUE_CLAIM = new Set();   // 'type|room' -> [{ id, from }] front first; crew id -> their spot (null: past the spots); crew id -> when they came into the room; the places those ahead of you are going to. Made 4 times a second
let QUEUE_YOU = null, QUEUE_AT = null, QUEUE_T = 0, QUEUE_D = null;   // QUEUE_T, QUEUE_D: the lines are made again 4 times a second, and on a new deck; you in a line: { type, kind, room, deck, at, title, flavour, k, tile, face, there, retry }; the made spots
const queueOrd = n => n + (n % 100 >= 11 && n % 100 <= 13 ? 'th' : ['th', 'st', 'nd', 'rd'][n % 10] || 'th');
function queueText(kind, fill, or) {                     // the head writer's line (LINES[kind]), else ours
  const L = typeof LINES !== 'undefined' && LINES[kind], e = Array.isArray(L) && L.length ? L[SHIP.time.day % L.length] : null;
  return (e && typeof e.text === 'string' ? e.text : or).replace(/\{(\w+)\}/g, (m, x) => fill[x] !== undefined ? fill[x] : m);
}
function queueSpots(type, room) {                        // the spot ids of that room's line, front first (made once a deck)
  if (!QUEUE_AT || QUEUE_AT.d !== deckDef) { QUEUE_AT = new Map(); QUEUE_AT.d = deckDef; QUEUE_AT.lines = new Map(); }
  const key = type + '|' + room; if (QUEUE_AT.lines.has(key)) return QUEUE_AT.lines.get(key);
  const pls = (deckDef.places || []).filter(q => q.room === room), mine = pls.filter(q => q.type === type);
  const out = type === 'shower' ? pls.filter(q => q.type === 'shower-queue').sort((a, b) => a.id < b.id ? -1 : 1).map(q => q.id) : [];
  const used = new Set((deckDef.places || []).map(q => placeSpot(q.id)).filter(sp => sp && sp.walk).map(sp => K(sp.walk)));
  const door = ([i, j]) => [[1, 0], [-1, 0], [0, 1], [0, -1]].some(([a, b]) => free(i + a, j + b) && roomAt(i + a, j + b) !== room && edgeOpen(i, j, i + a, j + b));
  const T = (ROOM_TILES[room] || []).filter(t => free(...t) && !used.has(K(t)) && !door(t)), open = new Set(T.map(K));
  const ws = mine.map(q => placeSpot(q.id)).filter(Boolean); if (!ws.length) { QUEUE_AT.lines.set(key, out); return out; }
  const cx = ws.reduce((a, sp) => a + sp.walk[0], 0) / ws.length, cz = ws.reduce((a, sp) => a + sp.walk[1], 0) / ws.length, far = t => Math.hypot(t[0] - cx, t[1] - cz);
  const last = out.length ? placeSpot(out[out.length - 1]) : null;
  let at = last ? last.walk : T.slice().sort((a, b) => far(a) - far(b) || a[0] - b[0] || a[1] - b[1])[0], dir = null;
  const seen = new Set(out.map(id => { const sp = placeSpot(id); return sp ? K(sp.walk) : ''; }));
  if (!last && at) { seen.add(K(at)); QUEUE_AT.set('@ql' + deckDef.num + '-' + key + '-0', { at, to: [cx, cz] }); out.push('@ql' + deckDef.num + '-' + key + '-0'); }
  while (at && out.length < QUEUE_MAX) {                 // away from the places, straight on where it can
    const nx = [[1, 0], [-1, 0], [0, 1], [0, -1]].map(([a, b]) => [at[0] + a, at[1] + b, a, b]).filter(([i, j]) => open.has(i + ',' + j) && !seen.has(i + ',' + j) && edgeOpen(at[0], at[1], i, j))
      .sort((m, n) => far(n) - far(m) || (dir && (n[2] === dir[0] && n[3] === dir[1]) - (m[2] === dir[0] && m[3] === dir[1])) || m[0] - n[0] || m[1] - n[1])[0];
    if (!nx) break;
    const id = '@ql' + deckDef.num + '-' + key + '-' + out.length; seen.add(nx[0] + ',' + nx[1]);
    QUEUE_AT.set(id, { at: [nx[0], nx[1]], to: at }); out.push(id); dir = [nx[2], nx[3]]; at = [nx[0], nx[1]];
  }
  QUEUE_AT.lines.set(key, out); return out;
}
function queueTick(dt, now) {
  const N = deckDef.num;
  if (QUEUE_YOU && (QUEUE_YOU.deck !== N || ACT)) queueOut(false);   // off the deck, or doing something else
  if ((QUEUE_T -= dt) > 0 && QUEUE_D === deckDef) { if (QUEUE_YOU) queueYou(dt, false); return; }
  QUEUE_T = .25; QUEUE_D = deckDef; QUEUE_NOW.clear(); QUEUE_SPOT.clear(); QUEUE_CLAIM.clear();
  const Y = QUEUE_YOU, seen = new Set();
  if (Y && Y.at === null && roomAt(...player.here()) === Y.room) Y.at = now;   // you're in the room: your place in the line from now
  const add = (type, room, e) => { const k = type + '|' + room; (QUEUE_NOW.get(k) || QUEUE_NOW.set(k, []).get(k)).push(e); };
  for (let i = 0; i < DECK_CREW.length; i++) {
    const a = DECK_CREW[i], w = whereIs(a.p, now); if (!w || w.deck !== N) continue;
    let type = QUEUE_TAGS[w.tag], pl = null, line = !!type;
    if (type) { const nx = whereIs(a.p, w.until); pl = nx && nx.placeId && PLACE_OF.get(nx.placeId); }
    else if (w.placeId && (w.type === 'callhome' || w.type === 'shower') && !(a.settled && a.spot && a.spot.id === w.placeId)) { pl = PLACE_OF.get(w.placeId); type = pl && pl.type; }   // on the way to one
    if (!pl || pl.type !== type) continue;
    if (!QUEUE_IN.has(a.p.id) && roomAt(...a.here()) === pl.room) QUEUE_IN.set(a.p.id, now);
    const from = QUEUE_IN.has(a.p.id) ? QUEUE_IN.get(a.p.id) : Infinity; seen.add(a.p.id);
    if (!line && pl.id !== PLAYER_PLACE && !(Y && Y.at !== null && Y.type === pl.type && Y.room === pl.room && from > Y.at)) { QUEUE_CLAIM.add(pl.id); continue; }   // theirs: unless it's the one you're using, or you were waiting first
    add(type, pl.room, { id: a.p.id, from });
  }
  for (const id of QUEUE_IN.keys()) if (!seen.has(id)) QUEUE_IN.delete(id);
  if (Y) add(Y.type, Y.room, { id: 'player', from: Y.at === null ? Infinity : Y.at });
  for (const [k, L] of QUEUE_NOW) {
    L.sort((x, y) => x.from - y.from || (x.id === 'player' ? 1 : y.id === 'player' ? -1 : x.id < y.id ? -1 : 1));
    const sp = queueSpots(...k.split('|')); for (let i = 0; i < L.length; i++) if (L[i].id !== 'player') QUEUE_SPOT.set(L[i].id, sp[i] || null);
  }
  if (QUEUE_YOU) queueYou(dt, true);
}
function queueOf(type) {
  let k = null; for (const key of QUEUE_NOW.keys()) if (key.startsWith(type + '|') && (!k || QUEUE_YOU && key === QUEUE_YOU.type + '|' + QUEUE_YOU.room)) k = key;
  const ids = k ? QUEUE_NOW.get(k).filter(e => e.from < Infinity).map(e => e.id) : []; return { ids, you: ids.indexOf('player') };
}
// you, in a line: walk up as it moves, a word when your place changes, and the first free one is yours at the front
// (fresh: the lines were just made, so who's ahead and where they're going is up to date)
function queueYou(dt, fresh) {
  const Q = QUEUE_YOU, L = QUEUE_NOW.get(Q.type + '|' + Q.room) || [], k = L.findIndex(e => e.id === 'player'), pp = player.obj.position;
  if (player.steer || player.goal && Q.tile && K(player.goal) !== K(Q.tile) || Q.there && !player.path.length && Q.tile && Math.hypot(cellPos(...Q.tile).x - pp.x, cellPos(...Q.tile).z - pp.z) > 1.5) { queueOut(true); return; }   // walked off
  if (fresh && k === 0 && Q.at !== null) {
    const pl = [...PLACE_OF.values()].find(q => q.type === Q.type && q.room === Q.room && !(PRIVATE_TYPES.has(q.type) && privatePlace(q)) && !BUSY.has(q.id) && !QUEUE_CLAIM.has(q.id) && !(heldBy(q.id) && !QUEUE_SPOT.has(heldBy(q.id).p.id)));
    if (pl) {
      QUEUE_YOU = null; player.stop();
      const pose = (typeof poseOf === 'function' ? poseOf(pl) : null) || pl.anim || (Q.kind === 'call' ? 'call' : PLAYER_ACTS[Q.kind].pose);
      actStart(Q.kind, pl.id, { pose, title: Q.title, flavour: Q.flavour, after: queueText('queue.go', {}, 'Your turn.') });
      return;
    }
  }
  if (fresh && Q.at !== null && k !== Q.k) { Q.k = k; toast(Q.title, k === 0 ? queueText('queue.next', {}, 'You\'re next in line.') : queueText(Q.type === 'shower' ? 'queue.shower' : 'queue.booth', { nth: queueOrd(k + 1) }, 'You\'re {nth} in line' + (Q.type === 'shower' ? ' for a shower.' : ' for a booth.'))); }
  let id = queueSpots(Q.type, Q.room)[k], sp = id && placeSpot(id);
  if (!sp && Q.at === null) { const dt0 = washDoorTiles(Q.room)[0]; if (dt0) sp = { walk: dt0, face: player.face }; }   // the line's full: just inside the door, so you're in the room and in it (the reviewer, 0.71.6)
  if ((Q.retry -= dt) > 0 || !sp || Q.tile && K(Q.tile) === K(sp.walk)) return;
  Q.retry = .5; if (K(player.here()) === K(sp.walk)) { Q.tile = sp.walk.slice(); Q.there = true; return; }
  if (playerGo(sp.walk, () => { if (QUEUE_YOU !== Q) return; Q.there = true; player.face = player.obj.rotation.y = sp.face; })) { Q.tile = sp.walk.slice(); Q.there = false; }
}
// from section 15's tap when every booth or shower near it is in use: into that room's line (true: handled)
function queueJoin(kind, pl, it) {
  if (!pl || !QUEUE_KINDS_OK.has(pl.type)) return false;
  if (QUEUE_YOU && QUEUE_YOU.type === pl.type && QUEUE_YOU.room === pl.room) { QUEUE_YOU.k = -1; return true; }   // in it already: your place again
  if (ACT) actEnd(true);                                 // sat down, on a call, on your way somewhere: you stop that to queue (the reviewer, 0.71.6)
  QUEUE_YOU = { type: pl.type, kind, room: pl.room, deck: deckDef.num, at: null, title: it.t, flavour: it.x, k: -1, tile: null, face: 0, there: false, retry: 0 };
  toast(it.t, queueText('queue.join', {}, pl.type === 'shower' ? 'Both showers are busy, so you join the line.' : 'Every booth is busy, so you join the line.'));
  return true;
}
const QUEUE_KINDS_OK = new Set(Object.values(QUEUE_TAGS));
function queueOut(walked) {
  const Q = QUEUE_YOU; QUEUE_YOU = null;
  if (Q && walked) toast(Q.title, queueText('queue.left', {}, 'You left the line.'));
}
function lineSpotMake(id) {
  const ql = QUEUE_AT && QUEUE_AT.d === deckDef && QUEUE_AT.get(id);   // a line at the booths or the showers (queueSpots)
  if (ql) { const c = cellPos(...ql.at), to = ql.to.length ? cellPos(ql.to[0], ql.to[1]) : c; return { id, walk: ql.at, x: c.x, z: c.z, y: 0, face: Math.atan2(to.x - c.x, to.z - c.z), pose: 'stand', anim: null, room: roomAt(...ql.at), onTile: true }; }
  const q = /^@wq-(\w+)-(\d+)$/.exec(id); if (q) { const at = washDoorTiles(q[1])[+q[2]]; if (!at) return null; const c = cellPos(...at);
    return { id, walk: at, x: c.x, z: c.z, y: 0, face: 0, pose: 'stand', anim: null, room: q[1], onTile: true }; }
  const m = /^@line-(\d+)$/.exec(id), at = m && LINE_AT[+m[1]]; if (!at) return null;
  const c = cellPos(...at), to = cellPos(...LINE_AT[+m[1] - 1]);   // facing the one ahead
  return { id, walk: at, x: c.x, z: c.z, y: 0, face: Math.atan2(to.x - c.x, to.z - c.z), pose: 'stand', anim: null, room: 'M', onTile: true };
}
const servLine = () => LINE.slice(), lineFront = id => { const k = LINE.indexOf(id); return k >= 0 && k < LINE_COUNTER; };
function lineJoin(id) { if (!LINE.includes(id)) LINE.push(id); return lineSpot(id); }
function lineLeave(id, gaveUp) { const k = LINE.indexOf(id); if (k < 0) return; LINE.splice(k, 1); if (gaveUp) LINE_LOG.left++; }
function lineSpot(id) {                                 // where to stand now: world x, z, face (radians, as the crew), the tile, and front (at the servery)
  const k = LINE.indexOf(id), sp = k >= 0 && lineSpotId(k) && placeSpot(lineSpotId(k)); if (!sp) return null;
  return { x: sp.x, z: sp.z, face: sp.face, at: sp.walk.slice(), front: k < LINE_COUNTER };
}
// once a frame: the first LINE_COUNTER in the line stand along the servery and are served there, each after their
// own serving time (timed from reaching it; stepping up between those spots keeps the clock), when there's food
function lineTick(dt, now) {
  lineCounter(now);
  const mins = typeof galleyServeMins === 'function' ? galleyServeMins(now) : LINE_SERVE;
  for (let k = 0; k < Math.min(LINE_COUNTER, LINE.length); k++) {
    const f = LINE[k]; if (f === 'player') continue;    // you're served by section 15
    const a = DECK_CREW.find(o => o.p.id === f);
    if (!a || !a.meal || a.meal.served) { LINE.splice(k--, 1); continue; }   // gone (the lift, a skip)
    const at = LINE_Q.indexOf(a.goalId), sp = at >= 0 && at < LINE_COUNTER && a.spot;
    if (!sp || Math.hypot(sp.x - a.x, sp.z - a.z) > 1.2) { a.lineT = 0; continue; }
    a.lineT = (a.lineT || 0) + dt * SHIP_RATE;
    if (a.lineT >= mins && (typeof galleyCanServe !== 'function' || galleyCanServe(now))) { LINE.splice(k--, 1); a.lineT = 0; a.served(whereIs(a.p, now), now); }
  }
}
// crewHold(p, placeId) keeps someone at a place on this deck (null: where they're headed now, or stood) whatever their
// plan says, until the function it returns is called (or crewHold(p, undefined)); for a game of Tiles with you (section
// 23, 0.26.31) and anything else that needs someone to stay put. Their plan runs on underneath: let go, they rejoin it.
const CREW_HELD = new Map();
function crewHold(p, placeId) {
  const id = p && (p.id || p); if (!id) return () => {};
  if (placeId === undefined) { CREW_HELD.delete(id); return () => {}; }
  CREW_HELD.set(id, placeId); return () => { if (CREW_HELD.get(id) === placeId) CREW_HELD.delete(id); };
}
// crewMakeWay(tile, mins) clears any tile for you (0.26.36; a shared tile clears by itself, sharedTile): crew whose place stands on it, or who stand on it, step to an
// open tile beside it in the same room and wait there, until the function it returns is called or `mins` ship minutes
// pass (default 10). For section 15 before walking you to a place that shares its tile with a crew station (the galley
// cook at 3-galley-2 stands on 3-range-1's panel tile [39, 4]). Cleared with the deck
const CREW_WAY = new Map();                              // tile key -> until (ship minutes)
function crewMakeWay(tile, mins = 10) {
  if (!Array.isArray(tile)) return () => {};
  const k = K(tile), until = shipNow() + mins; CREW_WAY.set(k, until);
  return () => { if (CREW_WAY.get(k) === until) CREW_WAY.delete(k); };
}
// a tile two places on this deck share as their walk-to tile (the galley cook's station 3-galley-2 on 3-range-1's
// panel): a crew member settled there makes way while you head for it or use a place on it (the lead, 0.26.36)
let SHARED_T = null;
function sharedTile(t) {
  if (!SHARED_T || SHARED_T.d !== deckDef) { const n = new Map(); for (const pl of PLACE_OF.values()) { const sp = placeSpot(pl.id), k = sp && K(sp.walk); if (k) n.set(k, (n.get(k) || 0) + 1); }
    SHARED_T = new Set([...n].filter(([, c]) => c > 1).map(([k]) => k)); SHARED_T.d = deckDef; }
  return !!t && SHARED_T.has(K(t));
}
function crewWayOn(now) {
  for (const [k, u] of CREW_WAY) if (u <= now) CREW_WAY.delete(k);
  const ps = PLAYER_PLACE && placeSpot(PLAYER_PLACE);   // your place's walk-to tile only while you stand on it (a station): sat in a mess seat you're off it, and the diner next to you needs it to sit down (0.71.0)
  const you = [player.path.length && player.goal, ps && ps.onTile && ps.walk].filter(t => t && sharedTile(t));
  if (!you.length) return CREW_WAY.size ? CREW_WAY : null;
  const out = new Map(CREW_WAY); for (const t of you) out.set(K(t), now + 1); return out;
}
function asideTile(at, way) {                            // an open tile next to `at`, same room, not one being kept clear
  const rm = roomAt(...at);
  for (let r = 1; r <= 2; r++) for (let di = -r; di <= r; di++) for (let dj = -r; dj <= r; dj++) {
    if (Math.max(Math.abs(di), Math.abs(dj)) !== r) continue;
    const t = [at[0] + di, at[1] + dj]; if (free(...t) && !way.has(K(t)) && roomAt(...t) === rm) return t;
  }
  return null;
}
const liftTiles = () => (ROOM_TILES['@'] || []).slice().sort((a, b) => a[1] - b[1] || a[0] - b[0]);
class CrewAgent {
  constructor(p, cell) {
    this.p = p; this.h = crowd.add(rosterSpec(p));
    const c = cellPos(...cell); this.x = c.x; this.z = c.z; this.y = 0;
    this.face = idHash(p.id) % 628 / 100; this.pose = 'stand';
    this.path = []; this.spot = null; this.goalId = undefined; this.settled = false; this.talking = 0;
    this.stuck = 0; this.stuckMax = 0; this.lastX = this.x; this.lastZ = this.z; this.noPath = 0;
    const bed = PLACE_OF.get(p.bed); this.bedRooms = bed ? [bed.room] : []; this.rooms = new Set(this.bedRooms);
    this.liftCell = (() => { const l = liftTiles(); return l.length ? l[idHash(p.id) % l.length] : cell; })();
  }
  here() { return cellAt(this.x, this.z); }
  // head for a place (an id), the lift ('@lift'), or nowhere in particular (null: stay on an open tile)
  retarget(goalId) {
    // set off from the place you're at (or sliding into): its walk-to tile, never the seat's own tile
    const atSpot = this.spot && (this.settled || !this.path.length);
    let from = atSpot ? this.spot.walk : this.here();
    if (!free(...from)) from = nearestOpen(this.x, this.z, null) || from;
    if (atSpot && !this.spot.onTile || !free(...this.here())) { const w = cellPos(...from); this.x = w.x; this.z = w.z; }   // up from the seat
    this.goalId = goalId; this.path = [];
    this.settled = false; this.spot = null;
    let goal = null;
    if (goalId === '@lift') goal = this.liftCell;
    else if (goalId) { this.spot = placeSpot(goalId); goal = this.spot && this.spot.walk; if (this.spot) this.rooms = new Set(this.bedRooms.concat(this.spot.room)); }
    if (!goal) { goal = free(...from) ? from : nearestOpen(this.x, this.z, null); if (!goal) return; }
    const inMess = this.meal && this.meal.tray && roomAt(...from) === 'M' && roomAt(...goal) === 'M';   // a tray stays in the mess hall: no short cut along the promenade (0.26.31)
    const path = (inMess && crewPath(from, goal, new Set([...this.rooms, 'M']), this, messOnly())) || crewPath(from, goal, new Set([...this.rooms, roomAt(...from)]), this);   // you can always leave the room you're in
    if (path) this.path = path;
    else { this.noPath++; this.lost = { from, goal, goalId, at: hhmm(SHIP.time.min) }; const c = cellPos(...goal); this.x = c.x; this.z = c.z; }   // no way there: they're simply there
  }
  update(dt, now, N) {
    const w = whereIs(this.p, now);
    if (w && w.escort && !(w.escort.mode === 'wait' && w.placeId)) return this.escortStep(dt, w.escort);   // section 21's escort: lead, follow or wait, with you (waiting at a place: they sit or stand there, below)
    this.esc = null;
    if (seekWho(this.p)) return this.seekStep(dt);         // section 20's walk-up: coming over for a word, then standing by you (0.71.0)
    if (w && w.visit && !w.visit.arrived && this.spot && (this.spot.id === w.visit.placeId || this.alt && this.alt[0] === w.visit.placeId && this.spot.id === this.alt[1]) && this.settled) {   // a visit: there (or at the next seat, when theirs was taken)
      w.visit.arrived = true; if (w.visit.onArrive) { try { w.visit.onArrive(this); } catch (e) { /* the caller's problem */ } }
    }
    this.hold = w && w.hold || (this.meal && this.meal.tray ? 'tray' : null);   // something in hand: a hover cart on a run (section 17's whereIs), your tray (mealStep)
    if (this.talking > 0) {                              // stopped for a word with you
      this.talking -= dt;
      if (!this.settled) { this.pose = 'stand'; this.face = Math.atan2(player.obj.position.x - this.x, player.obj.position.z - this.z); }
      if (!((this.rk || this.settled && this.spot && this.spot.mv) && recCrewSet(this, dt))) this.h.set({ x: this.x, y: this.y, z: this.z }, this.face, heldPose(this)); return true;
    }
    let goalId;
    if (w.deck !== N) goalId = '@lift';
    else if (w.act === 'commute') { const nx = whereIs(this.p, w.until); goalId = nx.deck === N ? nx.placeId || null : '@lift'; }
    else goalId = w.placeId || (w.tag === 'showerq' ? showerQSpot(this, w) : null);   // the shower queue with no place: inside the washroom door
    if (goalId !== '@lift' && QUEUE_SPOT.get(this.p.id)) goalId = QUEUE_SPOT.get(this.p.id);   // past the line's last spot: the old way (inside the washroom door, or where they are)   // in a line at the booths or the showers, in turn (queueTick, 0.71.4)
    this.tag = w.placeId === goalId ? w.tag || null : null;   // what they'll do there (the plan's tag)
    const mg = this.mealStep(w, now, N);                 // the servery line and the tray, inside the mess hall (0.26.30)
    if (mg !== undefined) { goalId = mg; this.tag = null; }
    if (goalId && (goalId === PLAYER_PLACE || BUSY.has(goalId) && !(this.settled && this.spot && this.spot.id === goalId))) goalId = this.elsewhere(goalId);   // you're using it (section 15), or someone's sat there: another seat, else wait nearby
    const held = CREW_HELD.get(this.p.id);
    if (held !== undefined) { goalId = held || (this.goalId !== '@lift' ? this.goalId : null); this.tag = null; }   // crewHold: kept here, whatever the plan says
    const way = crewWayOn(now);                          // crewMakeWay: off a tile you're heading for, waiting beside it
    if (way && goalId !== '@lift') {
      const sp = goalId && placeSpot(goalId), here = this.here();
      if (sp && (sp.onTile || CREW_WAY.has(K(sp.walk))) && (way.has(K(sp.walk)) || way.has(K(cellAt(sp.x, sp.z)))) || !this.settled && way.has(K(here))) {   // standing at their place (the cook), not a diner whose seat shares a walk-to tile with yours (0.26.37)
        if (this.goalId !== '@aside') {
          const to = asideTile(here, way); this.retarget(null); this.goalId = '@aside';
          const pth = to && crewPath(this.here(), to, new Set([...this.rooms, roomAt(...this.here())]), this); if (pth) this.path = pth;
        }
        goalId = '@aside'; this.tag = null;
      }
    }
    if (goalId !== this.goalId) this.retarget(goalId);
    const ox = this.x, oz = this.z;
    if (this.path.length) {
      const c = cellPos(...this.path[0]), dx = c.x - this.x, dz = c.z - this.z, d = Math.hypot(dx, dz), st = CREW_SPEED * dt;
      if (d <= st) { this.x = c.x; this.z = c.z; this.path.shift(); }
      else { this.x += dx / d * st; this.z += dz / d * st; this.face = Math.atan2(dx, dz); }
      this.pose = 'walk'; this.y = 0;
    } else if (this.spot && !this.settled && spotTaken(this, this.spot.id)) { this.pose = 'stand';   // someone sat down in it first (this very frame, before BUSY knew: 0.36.91, day 3's 3-mess-42): wait on the walk-to tile; next frame finds another
    } else if (this.spot && !this.settled) {             // the last step, from the walk-to tile onto the spot itself
      const dx = this.spot.x - this.x, dz = this.spot.z - this.z, d = Math.hypot(dx, dz), st = CREW_SPEED * .8 * dt;
      if (d <= st) { this.x = this.spot.x; this.z = this.spot.z; this.settled = true; this.pose = crewPose(this); this.face = this.spot.face; this.y = this.spot.y; }
      else { this.x += dx / d * st; this.z += dz / d * st; this.face = Math.atan2(dx, dz); this.pose = 'walk'; }
    } else if (this.goalId === '@lift') return false;    // in the car: gone to another deck
    else if (!this.spot) this.pose = 'stand';
    // stuck: meant to be going somewhere and not getting there (in ship minutes)
    const going = this.path.length > 0 || (this.spot && !this.settled);
    if (going && Math.hypot(this.x - ox, this.z - oz) < 1e-4) { this.stuck += dt * SHIP_RATE; this.stuckMax = Math.max(this.stuckMax, this.stuck); } else this.stuck = 0;
    if ((this.rk || this.settled && this.spot && this.spot.mv) && recCrewSet(this, dt)) return true;   // 0.84.6: swimming the lane, up the wall (8c)
    this.h.set({ x: this.x, y: this.y, z: this.z }, this.face, heldPose(this));
    return true;
  }
  // someone's in your place: a free seat of the same kind close by (kept while the plan's place stays the same), else
  // stand nearby (null); not a seat: stand nearby (0.26.30, the lead: nobody stands about holding a tray)
  elsewhere(id) {
    const pl = PLACE_OF.get(id);
    if (!pl || !ALT_SEAT.has(pl.type)) return id === PLAYER_PLACE ? null : id;   // not a seat: wait nearby for you, and as before for anyone else
    if (this.alt && this.alt[0] === id && this.alt[1] !== PLAYER_PLACE && (!BUSY.has(this.alt[1]) || this.settled && this.spot && this.spot.id === this.alt[1])) return this.alt[1];
    const k = seatsBeside(id, 1, [pl.type])[0]; this.alt = k ? [id, k] : null; return k || null;
  }
  // a meal from the servery (0.26.30, the user's rule): whoever's plan has them at a servery-queue place walks to the
  // back of the line and joins it in the mess hall, steps up as the front is served, is served at the counter, then
  // goes where the plan goes next (a sit-down meal: its seat, with a tray if the seat's in the mess hall). When the
  // meal's over, the tray simply goes (no tray return, 0.36.85) and on they go. Undefined: follow the plan
  mealStep(w, now, N) {
    const eat = N === 3 && w.deck === 3 && (w.act === 'breakfast' || w.act === 'dinner'), key = eat ? w.act + Math.floor(w.from / 1440) : null;
    let m = this.meal;
    if (m && m.key !== key) {                            // over (or something else came up): out of the line, the tray gone
      const k = m.served ? -1 : LINE.indexOf(this.p.id);
      if (k >= 0 && now - (m.over || (m.over = now)) < LINE_LATE) return lineSpotId(k);   // already in the line: a little late for what's next (served, they go on)
      if (k >= 0) lineLeave(this.p.id);                  // but not for ever (an empty galley serves nobody): out, a missed meal (reviewer 1b, 0.26.33)
      if (!m.served && key === null && now - (m.over || (m.over = now)) < LINE_LATE) return this.mealLine(now);   // on the way (a grab stop is shorter than the walk): a little late for what's next
      if (!m.served) { LINE_LOG.left++; if (LINE_LOG.who.length < 8) LINE_LOG.who.push(this.p.id + ' ' + hhmm(now % 1440)); }
      if (m.tray) { m.tray = false; LINE_LOG.returned++; }   // left on the table: it goes with the meal
      m = this.meal = null;
    }
    if (!eat) return undefined;
    if (!m) {                                            // first seen during the meal: from the queue, or already eating
      const q = lineSeg(w);
      m = this.meal = { key, served: !q, tray: false };
      if (!q) {
        const pv = whereIs(this.p, w.from - .01), queued = !!(pv && pv.act === w.act && lineSeg(pv));
        if (queued && trayTo(w.placeId) && roomAt(...this.here()) !== 'M') m.served = false;   // up late (out of the lift): the line first, so a tray's only ever in the mess hall (the performance engineer, 0.26.34)
        else m.tray = queued && trayTo(w.placeId);
      }
    }
    if (!m.served) return this.mealLine(now);
    if (m.next !== undefined && lineSeg(w)) {            // served before the plan's queue time is up
      if (m.tray && m.next && BUSY.has(m.next) && !this.elsewhere(m.next)) { m.tray = false; m.trayLate = true; LINE_LOG.trays--; }   // the mess hall's full: no tray till they sit (seated diners show none; 0.26.32)
      return m.next;
    }
    // 0.27.47: the same after the queue: their seat still taken and no free one beside it (the Sunday table, day 35's
    // quist-ilse at 17:59), so they'd wait nearby holding a tray; no tray till they sit
    if (m.tray && !lineSeg(w) && w.placeId && BUSY.has(w.placeId) && !(this.settled && this.spot && this.spot.id === w.placeId) && !this.elsewhere(w.placeId)) { m.tray = false; m.trayLate = true; LINE_LOG.trays--; }
    if (m.trayLate && this.settled && this.spot && trayTo(this.spot.id)) { m.tray = true; m.trayLate = false; LINE_LOG.trays++; }
    if (m.seat && !w.placeId) return m.seat;             // no seat planned: the one picked at the counter
    return undefined;
  }
  mealLine(now) {                                        // to the back of the line; in it, your place in it
    let k = LINE.indexOf(this.p.id);
    const back = k < 0 && lineSpotId(LINE.length) && placeSpot(lineSpotId(LINE.length));   // join on reaching the back (past the spots: in the mess hall)
    if (k < 0 && roomAt(...this.here()) === 'M' && (!back || Math.hypot(back.x - this.x, back.z - this.z) < 1.6)) { k = LINE.length; LINE.push(this.p.id); LINE_LOG.joined++; LINE_LOG.long = Math.max(LINE_LOG.long, LINE.length); }
    if (k >= 0 && !this.lineAt) this.lineAt = now;
    return lineSpotId(k < 0 ? LINE.length : k);
  }
  served(w, now) {                                       // at the counter (lineTick): food, and on to the plan's next place
    const m = this.meal; if (!m) return;
    m.served = true; LINE_LOG.served++; LINE_LOG.wait = Math.max(LINE_LOG.wait, now - (this.lineAt || now)); this.lineAt = 0;
    let nx = w; while (lineSeg(nx) && nx.act === w.act) nx = whereIs(this.p, nx.until);   // past the walk-in and the queue stop
    const same = nx.act === w.act && w.act + Math.floor(w.from / 1440) === m.key && nx.deck === 3;
    m.tray = same && trayTo(nx.placeId);
    if (lineSeg(w)) m.next = nx.deck !== 3 || nx.act === 'commute' ? '@lift' : nx.placeId || (same ? seatsBeside(LINE_Q[0], 1, ['mess-seat'])[0] || null : null);   // a meal with no seat planned: the nearest free one
    if (same && !nx.placeId && m.next) { m.tray = true; m.seat = m.next; }
    if (m.tray) LINE_LOG.trays++;
  }
  // the escort (Pillar 4, section 21's escortPlan): 'lead' walks to `to` (a place id or a [c, r] tile) and stops,
  // facing you, while you're more than ESC_WAIT tiles behind (on again within ESC_GO); 'follow' keeps about ESC_NEAR
  // tiles from you; 'wait' stands at `to` (or where they are). Paths are made again when the goal moves (you, or a new
  // `to`), at most twice a second. They may go anywhere you can (the rooms on their way are allowed)
  escortStep(dt, e) {
    if (e.scene) this.hold = e.hold || null;             // a stage direction's box (crewScene, 0.71.2); escorts as before
    const pp = e.after ? e.after : player.obj.position, dist = Math.hypot(pp.x - this.x, pp.z - this.z), you = cellAt(pp.x, pp.z);
    const goal = e.mode === 'follow' ? you : escortGoal(e, this);
    const key = e.mode + '|' + (goal ? goal.join(',') : '-');
    this.escT = (this.escT || 0) - dt;
    if (key !== this.esc && (this.escT <= 0 || !this.esc || this.esc.split('|')[0] !== e.mode)) {
      this.esc = key; this.escT = .5; this.goalId = '@escort'; this.settled = false; this.spot = null; this.path = [];
      let from = this.here(); if (!free(...from)) from = nearestOpen(this.x, this.z, null) || from;
      if (goal) { const p = crewPath(from, goal, new Set([...this.rooms, roomAt(...from), roomAt(...goal)]), this); if (p) this.path = p; }
    }
    if (e.mode !== 'lead' || dist < ESC_GO) this.escHeld = false;
    else if (dist > ESC_WAIT) this.escHeld = true;
    const near = e.mode === 'follow' && dist <= ESC_NEAR;
    if (this.path.length && !this.escHeld && !near) {
      const c = cellPos(...this.path[0]), dx = c.x - this.x, dz = c.z - this.z, d = Math.hypot(dx, dz), st = CREW_SPEED * (e.pace || 1) * dt;   // pace: section 21's stroll
      if (d <= st) { this.x = c.x; this.z = c.z; this.path.shift(); } else { this.x += dx / d * st; this.z += dz / d * st; this.face = Math.atan2(dx, dz); }
      this.pose = 'walk';
    } else { this.pose = 'stand'; this.face = Math.atan2(pp.x - this.x, pp.z - this.z); }   // waiting: look at you
    this.y = 0; this.stuck = 0; this.tag = 'escort';
    this.h.set({ x: this.x, y: this.y, z: this.z }, this.face, heldPose(this));
    return true;
  }
  // section 20's walk-up (0.71.0): over to you (re-aimed as you move), then standing by you, facing you, while the chip is up
  seekStep(dt) {
    const pp = player.obj.position, dist = Math.hypot(pp.x - this.x, pp.z - this.z);
    if (this.goalId !== '@seek') { this.retarget(null); this.goalId = '@seek'; this.seekKey = null; this.seekNear = false; }   // up from a seat first
    this.seekT = (this.seekT || 0) - dt;
    const go = dist > SEEK_BESIDE + (this.seekNear ? .8 : 0); this.seekNear = !go;
    if (go) {
      const you = cellAt(pp.x, pp.z), goal = free(...you) ? you : nearestOpen(pp.x, pp.z, null), key = goal ? K(goal) : '-';
      if (goal && key !== this.seekKey && (this.seekT <= 0 || !this.path.length)) {
        this.seekKey = key; this.seekT = .5; let from = this.here(); if (!free(...from)) from = nearestOpen(this.x, this.z, null) || from;
        this.path = crewPath(from, goal, new Set([...this.rooms, roomAt(...from), roomAt(...goal)]), this) || [];
      }
    } else { this.path = []; this.seekKey = null; }
    if (this.path.length) {
      const c = cellPos(...this.path[0]), dx = c.x - this.x, dz = c.z - this.z, d = Math.hypot(dx, dz), st = CREW_SPEED * dt;
      if (d <= st) { this.x = c.x; this.z = c.z; this.path.shift(); } else { this.x += dx / d * st; this.z += dz / d * st; this.face = Math.atan2(dx, dz); }
      this.pose = 'walk';
    } else { this.pose = 'stand'; this.face = Math.atan2(pp.x - this.x, pp.z - this.z); }
    if (!go && SEEK_COME && SEEK_COME.p === this.p) seekArrive(this);
    this.y = 0; this.stuck = 0; this.settled = false; this.tag = null;
    this.h.set({ x: this.x, y: this.y, z: this.z }, this.face, heldPose(this));
    return true;
  }
  remove() { if (this.h.full) this.h.dispose(); else crowd.remove(this.h); }
}
const ESC_WAIT = 4, ESC_GO = 3, ESC_NEAR = 2;          // tiles: the escort waits for you, sets off again, keeps this close
// seatsBeside(placeId, n = 2, types): the n free seats on this deck nearest a place (yours: playerHolds()), nearest
// first, for sitting someone at your table (section 21: the escort waits at one, crewComeTo sends Calder to another).
// Free: nobody settled there, nobody heading there, not yours. Types default to mess and lounge seats and benches
function seatsBeside(placeId, n = 2, types = ['mess-seat', 'lounge-seat', 'bench']) {
  const at = placeId && PLACE_OF.get(placeId); if (!at) return [];
  const xy = q => q.xy || [q.at[0] + .5, q.at[1] + .5], [x, z] = xy(at);
  const busy = new Set([placeId, PLAYER_PLACE].concat(DECK_CREW.map(a => a.spot && a.spot.id), DECK_CREW.map(a => a.meal && a.meal.next)));   // and a seat a served diner is about to walk to (0.36.91)
  // nor a seat shipDay holds for the arrival dinner now ('intro:<id>': yours, Torres's, the Chief's), even while it's empty
  // because Torres is still showing you round (reviewer 1c's paced tour, 0.26.39)
  const now = shipNow(), res = typeof shipDay === 'function' ? shipDay(Math.floor(now / 1440) + 1).occ.res : null;
  const held = id => !!res && (res.get(id) || []).some(([x, y, ev]) => String(ev).startsWith('intro:') && x <= now && now < y);
  return (deckDef.places || []).filter(q => types.includes(q.type) && !busy.has(q.id) && !BUSY.has(q.id) && !held(q.id))
    .map(q => [q.id, Math.hypot(xy(q)[0] - x, xy(q)[1] - z)]).sort((a, b) => a[1] - b[1] || (a[0] < b[0] ? -1 : 1)).slice(0, n).map(e => e[0]);
}
// where the escort heads, as a tile on this deck: `to` is a place id, a [c, r] tile, { deck, tile } or { deck, room }
// (the room's open tile nearest them); on another deck, leading means to the lift (waiting means staying put)
function escortGoal(e, a) {
  const to = e.to, N = deckDef.num;
  if (!to) return null;
  if (typeof to === 'string') { const sp = placeSpot(to); return sp ? sp.walk : null; }
  if (Array.isArray(to)) return to;
  if (to.deck != null && to.deck !== N) return e.mode === 'lead' ? a.liftCell : null;
  if (Array.isArray(to.tile)) return to.tile;
  const tiles = to.room && ROOM_TILES[to.room];
  if (!tiles || !tiles.length) return null;
  return tiles.reduce((b, t) => { const c = cellPos(...t), d = Math.hypot(c.x - a.x, c.z - a.z); return d < b[1] ? [t, d] : b; }, [null, Infinity])[0];
}
// Story crew close to you get a full rig (makeCharacter, baked) instead of a crowd body: FULL_MAX of them at most,
// within FULL_NEAR tiles, back to the crowd beyond FULL_FAR. A FullPerson takes the crowd's set() and its posing
// update() (sit, lie, work) as they are, so the two look and move the same; it borrows them from CrowdPerson,
// so it relies on CrowdPerson's fields (g, k, pos, face, rot, pose, phase, moved, fresh, eat, eatT, rnd).
const FULL_MAX = 3, FULL_NEAR = 4.5, FULL_FAR = 6;
class FullPerson {
  constructor(spec, id) {
    this.rig = makeCharacter(spec); this.spec = this.rig.spec; this.h = this.spec.height;
    this.rig.root.rotation.order = 'YXZ'; scene.add(this.rig.root); this.full = true;
    let sd = idHash(id) % 2147483646 + 1; this.rnd = () => (sd = (sd * 16807) % 2147483647) / 2147483647;
    this.g = { p: 0, w: 0, turn: 0, look: 0, lookT: this.rnd() * 3, tail: 0, tailV: 0, lean: 0, t0: this.rnd() * 20 };
    this.k = { sit: 0, lie: 0, work: 0 }; this.eat = 0; this.eatT = 2 + this.rnd() * 6;
    this.pos = new THREE.Vector3(); this.face = 0; this.rot = 0; this.pose = 'stand'; this.phase = undefined; this.moved = 0; this.fresh = true;
  }
  dispose() { scene.remove(this.rig.root); this.rig.root.traverse(o => { if (o.isMesh) o.geometry.dispose(); }); }
}
FullPerson.prototype.set = CrowdPerson.prototype.set;
FullPerson.prototype.update = CrowdPerson.prototype.update;

