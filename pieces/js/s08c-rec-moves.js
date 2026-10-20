// =====================================================================
// 8c. REC DECK MOVES (the rec deck animation engineer, 0.81.x; plans/recdeck-plan.html sections 8 and 9)
// The player's poses for the rec deck, on any rig (8b's ACTS): swim (front crawl), tread (chest-deep, sculling),
// kayak (seated in a kayak, a double paddle, a helmet), climb / ring / lower (up the wall in a harness, ringing the
// bell, lowered by the auto-belay), float (slow bounces, somersaults, a star shape), and seated or standing cheer, clap
// and groan for the stands and the auditorium. '+towel' is a towel over the shoulder after a swim.
// An activity with a `root` function moves the whole body too (in the water, up the wall, tumbling), after the base
// pose has placed it: CrowdPerson.update calls recRoot only for someone who has used one (o.rootOn), so nobody else
// changes. Props come from PROP_KIT on first use (no R(), colours through col()); the kayak rides the body bone, the
// paddle and helmet the chest, the harness the chest; the belay line is one thin mesh on the stand-in while it climbs.
// The rec kit is makeCharacter's kit: 'rec' (REC_KIT): a colour change, no extra draw calls. playerKit(k) changes yours.
//
// The mover (for section 15's activities): actStart(kind, placeId, { move: M }) walks you to the place as usual; in
// the 'do' phase recMoveStep drives the stand-in along M and the activity ends when M is done. M is in DECK
// coordinates like a place's xy ([20.5, 9.5] is tile [20, 9]'s centre), heights in metres above the deck floor:
//   { kind: 'swim',  path: [[x, z], [x, z]], y: water top, lengths: 4 }      one lane, end to end; the point is the
//                                                                          swimmer's chest, so keep ends ~.7 from the walls
//   { kind: 'tread', at: [x, z], y: water top, face }                       until the activity's minutes are done
//   { kind: 'kayak', path: [[x, z, fast?], ...], y: water top, laps: 1 }    a loop, closed for you; fast: 1 on white water
//   { kind: 'climb', at: [x, z], face, top: metres, onRing() }              at: the foot of the route, against the wall;
//                                                                          face: toward the wall ('n', 's', 'e', 'w' or degrees)
//   { kind: 'float', at: [x, z], r: drift radius, top: metres, bounces }     grip socks on (the stand-in only)
// Leave out lengths, laps or bounces and the move goes on until the activity's minutes are up, then stops at its
// next natural end (back at the lane's start, the loop's start, the floor). Nothing here calls R().
// =====================================================================
Object.assign(HOLDS, { towel: { prop: 'towel', bone: 'C', one: 2 } });   // over the left shoulder; one: 2 is neither arm, so both swing as usual
for (const a of ['cheer', 'clap', 'groan', 'slump']) ACT_SEATED.add(a);
Object.assign(PROP_KIT, {
  kayak(p) {                                             // on the body bone, in metres from the root: the hull's waterline at .66
    part(p, GEO.sph, '#f2a33a', 0, .66, .32, .34, .15, 1.38); part(p, GEO.sph, '#e05a3a', 0, .73, .32, .2, .09, 1.2);
    part(p, torG(.21, .03), '#2b2f33', 0, .79, .02, 1, 1.3, 1, Math.PI / 2);
  },
  paddle(p) {                                            // on the chest: the shaft across the hands, a blade each end; and the helmet
    part(p, GEO.box, '#2b2f33', 0, .1, .4, 1.3, .024, .024);   // 0.80.9 (the user's: too big for the kayak): 1.3 long, was 2.0
    for (const x of [-1, 1]) part(p, GEO.sph, '#e9c46a', x * .69, .1, .4, .13, .065, .02, 0, x * .5, 0);
    part(p, capG(.19, Math.PI * .56), '#d8432f', 0, .535, -.01, 1, 1.02, 1.05, -.2);
    part(p, GEO.box, '#2b2f33', 0, .6, .17, .2, .02, .06, .3);
  },
  harness(p) {                                           // on the chest: the waist belt, the leg loops' straps, the belay loop in front
    part(p, torG(.17, .022), '#2b2f33', 0, -.07, 0, 1, 1, 1.02, Math.PI / 2);
    for (const x of [-.07, .07]) part(p, GEO.box, '#e8a33a', x, -.14, .15, .03, .12, .025, .3);
    part(p, torG(.035, .012), '#f0795a', 0, -.11, .19);
  },
  towel(p) {                                             // on the chest: over the left shoulder, down the front and the back
    for (const z of [1, -1]) part(p, GEO.box, '#f4f1ea', .16, .17, z * .19, .12, .28, .022, z * -.12);
    part(p, GEO.sph, '#f4f1ea', .17, .33, 0, .075, .04, .2); part(p, GEO.box, REC_KIT.coral, .16, .0724, .2179, .122, .03, .008, -.12);   // on the front piece's face, tilted with it
  },
});
const REC_ACTS = {
  swim: { root(o, root, s, t) {                          // face down along the lane, the back just at the water; the point is the chest
    const h = o.h, th = (Math.PI / 2 - .1) * s, c = 1.0 * h * s;
    root.rotation.x = L(root.rotation.x, th, 1);
    root.position.x -= Math.sin(o.rot) * c; root.position.z -= Math.cos(o.rot) * c;
    root.position.y = L(root.position.y, o.pos.y - .2 * h + .015 * Math.sin(t * 3.4), s);
  }, f(r, s, t, b, ph) {
    const u = (t * .52 + ph) % 1;                        // one stroke each arm a cycle: pull under the body, recover over the back
    for (const a of r.arms) {
      const v = (u + (a.side > 0 ? .5 : 0)) % 1, ang = -Math.PI + 2 * Math.PI * v, rc = v > .5 ? Math.sin((v - .5) * 2 * Math.PI) : 0;
      a.sh.rotation.x = L(a.sh.rotation.x, ang, s); a.el.rotation.x = L(a.el.rotation.x, -.2 - 1.2 * rc, s);
      a.sh.rotation.z = L(a.sh.rotation.z, a.side * (.1 + .3 * rc), s); a.hand.rotation.x = L(a.hand.rotation.x, .25, s);
    }
    const roll = Math.sin(2 * Math.PI * u), br = pulse(t * .52 + ph, 2, .45);   // the body rolls with the stroke; a breath every other stroke
    r.hips.position.y = L(r.hips.position.y, HIP_Y, s); r.hips.rotation.y = L(r.hips.rotation.y, .12 * roll, s); r.hips.rotation.z = L(r.hips.rotation.z, 0, s);
    r.chest.rotation.y = L(r.chest.rotation.y, .38 * roll, s); r.torso.rotation.x = L(r.torso.rotation.x, 0, s);
    r.head.rotation.x = L(r.head.rotation.x, -.3, s); r.head.rotation.y = L(r.head.rotation.y, -.38 * roll + 1.0 * br, s);
    for (const leg of r.legs) {                          // a flutter kick, toes pointed
      const k = Math.sin(t * 8.5 + (leg.side > 0 ? 0 : Math.PI));
      leg.thigh.rotation.x = L(leg.thigh.rotation.x, .2 * k, s); leg.knee.rotation.x = L(leg.knee.rotation.x, .2 + .18 * k, s);
      leg.ankle.rotation.x = L(leg.ankle.rotation.x, 1.15, s); leg.thigh.rotation.z = L(leg.thigh.rotation.z, 0, s);
    }
  } },
  tread: { root(o, root, s, t) {                         // chest-deep, bobbing a little
    root.position.y = L(root.position.y, o.pos.y - 1.02 * o.h + .025 * Math.sin(t * 1.3), s);
  }, f(r, s, t, b, ph) {
    for (const a of r.arms) { const w = Math.sin(t * 2.6 + a.side * .8 + ph); armTo(a, s, -.4, -.5, .75 + .12 * w, .45 * w); }   // sculling
    for (const leg of r.legs) {                          // a slow eggbeater
      const th = t * 2.1 + (leg.side > 0 ? 0 : Math.PI) + ph;
      leg.thigh.rotation.x = L(leg.thigh.rotation.x, -.55 + .2 * Math.sin(th), s); leg.knee.rotation.x = L(leg.knee.rotation.x, 1.0 + .3 * Math.cos(th), s);
      leg.thigh.rotation.z = L(leg.thigh.rotation.z, leg.side * .22, s); leg.ankle.rotation.x = L(leg.ankle.rotation.x, .4, s);
    }
    r.head.rotation.x = L(r.head.rotation.x, -.08, s); r.head.rotation.y = L(r.head.rotation.y, .3 * Math.sin(t * .4 + ph), s);
  } },
  kayak: { props: { B: 'kayak', C: 'paddle' }, root(o, root, s, t) {   // sitting in the hull, which bobs and rocks
    root.position.y = L(root.position.y, o.pos.y - .66 + .02 * Math.sin(t * 1.9) * (o.fast ? 2.5 : 1), s);
    root.rotation.z = L(root.rotation.z, (o.fast ? .09 : .04) * Math.sin(t * 1.4), s);
    root.rotation.x = L(root.rotation.x, (o.fast ? .05 : .015) * Math.sin(t * 2.3), s);
  }, f(r, s, t, b, ph) {
    const w = Math.sin(t * 2.3 + ph);                     // the paddle dips one side, then the other
    r.hips.position.y = L(r.hips.position.y, HIP_Y, s); r.hips.rotation.y = L(r.hips.rotation.y, 0, s); r.hips.rotation.z = L(r.hips.rotation.z, 0, s);
    for (const leg of r.legs) {                          // legs out in front, inside the hull
      leg.thigh.rotation.x = L(leg.thigh.rotation.x, -1.42, s); leg.knee.rotation.x = L(leg.knee.rotation.x, .15, s);
      leg.ankle.rotation.x = L(leg.ankle.rotation.x, -.25, s); leg.thigh.rotation.z = L(leg.thigh.rotation.z, leg.side * .08, s);
    }
    r.torso.rotation.x = L(r.torso.rotation.x, .1, s);
    r.chest.rotation.y = L(r.chest.rotation.y, .42 * w, s); r.chest.rotation.z = L(r.chest.rotation.z, .3 * w, s);
    for (const a of r.arms) armTo(a, s, -1.2 - .22 * w * a.side, -.5, -.06, .2);
    r.head.rotation.x = L(r.head.rotation.x, 0, s); r.head.rotation.y = L(r.head.rotation.y, 0, s);   // still: the helmet rides the chest
  } },
  climb: { props: { C: 'harness' }, root(o, root, s) { root.position.y = L(root.position.y, o.pos.y, s); },
    f(r, s, t, b, ph) {                                  // one hand reaches up while the other pulls, the opposite foot steps up
      const u = (t * .85 + ph) % 2, side = u < 1 ? 1 : -1, q = ss(u % 1);
      for (const a of r.arms) { const k = a.side === side ? q : 1 - q; armTo(a, s, L(-2.15, -2.95, k), L(-1.5, -.2, k), .22, .3); }
      recLegs(r, s, side, q);
      r.torso.rotation.x = L(r.torso.rotation.x, .14, s); r.head.rotation.x = L(r.head.rotation.x, -.45, s); r.head.rotation.y = L(r.head.rotation.y, .25 * side * q, s);
    } },
  ring: { props: { C: 'harness' }, root(o, root, s) { root.position.y = L(root.position.y, o.pos.y, s); },
    f(r, s, t, b, ph) {                                  // at the top: hold on with the left, ring the bell with the right
      const [L_, R_] = [r.arms.find(a => a.side > 0), r.arms.find(a => a.side < 0)];
      armTo(L_, s, -2.9, -.25, .15, .3); armTo(R_, s, -2.7, -.35 + .3 * Math.sin(t * 15), .55, .2);
      recLegs(r, s, 1, .3);
      r.torso.rotation.x = L(r.torso.rotation.x, .1, s); r.head.rotation.x = L(r.head.rotation.x, -.6, s); r.head.rotation.y = L(r.head.rotation.y, -.3, s);
    } },
  lower: { props: { C: 'harness' }, root(o, root, s) {  // sitting back in the harness, feet on the wall, walking down it
    root.position.y = L(root.position.y, o.pos.y, s); root.rotation.x = L(root.rotation.x, -.42, s);
    root.position.x -= Math.sin(o.rot) * .32 * s; root.position.z -= Math.cos(o.rot) * .32 * s;
  }, f(r, s, t, b, ph) {
    for (const a of r.arms) armTo(a, s, -1.65, -1.25, -.08, .25);   // both hands on the line
    for (const leg of r.legs) {
      const w = Math.sin(t * 3.2 + (leg.side > 0 ? 0 : Math.PI) + ph);
      leg.thigh.rotation.x = L(leg.thigh.rotation.x, -1.15 + .22 * w, s); leg.knee.rotation.x = L(leg.knee.rotation.x, .75 - .3 * w, s);
      leg.ankle.rotation.x = L(leg.ankle.rotation.x, -.35, s); leg.thigh.rotation.z = L(leg.thigh.rotation.z, leg.side * .14, s);
    }
    r.torso.rotation.x = L(r.torso.rotation.x, .2, s); r.head.rotation.x = L(r.head.rotation.x, .35, s);
  } },
  float: { root(o, root, s) {                            // up off the floor; a somersault turns about the middle, not the feet
    const th = (o.spin || 0) * s, c = .78 * o.h;
    root.position.y = L(root.position.y, o.pos.y, s) + c * (1 - Math.cos(th));
    root.position.x -= Math.sin(o.rot) * c * Math.sin(th); root.position.z -= Math.cos(o.rot) * c * Math.sin(th);
    root.rotation.x += th;
  }, f(r, s, t, b, ph) {
    const st = r.star || 0, d = Math.sin(t * .7 + ph);    // drifting limbs, opening to a star at the top of a bounce
    for (const a of r.arms) armTo(a, s, L(-.7 + .3 * d * a.side, -.15, st), L(-.9 + .2 * d, -.08, st), L(.55, 1.5, st), .25 * Math.sin(t * 1.1 + a.side));
    for (const leg of r.legs) {
      const w = Math.sin(t * .9 + leg.side * 1.5 + ph);
      leg.thigh.rotation.x = L(leg.thigh.rotation.x, L(-.4 + .25 * w, 0, st), s); leg.knee.rotation.x = L(leg.knee.rotation.x, L(.7 + .3 * w, .05, st), s);
      leg.thigh.rotation.z = L(leg.thigh.rotation.z, leg.side * L(.12, .5, st), s); leg.ankle.rotation.x = L(leg.ankle.rotation.x, .35, s);
    }
    r.hips.position.y = L(r.hips.position.y, HIP_Y, s); r.torso.rotation.x = L(r.torso.rotation.x, .1 * (1 - st), s);
    r.head.rotation.x = L(r.head.rotation.x, -.25 + .2 * st, s);
    if (r.tail) r.tail.rotation.x = L(r.tail.rotation.x, -1.6, s);   // hair floats up
  } },
  cheer: { f(r, s, t, b, ph) {                           // arms up and pumping at a point
    const u = pulse(t, 2.2, 1.3, ph);
    for (const a of r.arms) armTo(a, s, L(-2.3, -2.95, u) + .12 * Math.sin(t * 8 + a.side), L(-1.0, -.15, u), .32, 0);
    r.torso.rotation.x = L(r.torso.rotation.x, -.06, s); r.head.rotation.x = L(r.head.rotation.x, -.22, s);
  } },
  clap: { f(r, s, t, b, ph) {                            // hands together in front, about three claps a second
    const c = Math.abs(Math.sin(t * 9.5 + ph));
    for (const a of r.arms) armTo(a, s, -.85, -1.05, L(-.42, -.12, c), .2);
    r.head.rotation.x = L(r.head.rotation.x, -.05, s);
  } },
  groan: { f(r, s, t, b, ph) {                           // a near miss: hands on the head, a look down
    for (const a of r.arms) armTo(a, s, -2.55, -2.25, .6, .4);
    r.head.rotation.x = L(r.head.rotation.x, .3 + .05 * Math.sin(t * 2), s); r.torso.rotation.x = L(r.torso.rotation.x, .1, s);
  } },
  slump: { f(r, s, t, b, ph, h, sy) {                   // 0.84.6 (rec engineer B): sat back in the seat, legs out, hands on the belly or behind the head
    if (b !== 'sit') return;                             // a seat with anim: 'slump' (poseOf gives 'sit:slump'); standing, nothing
    const hy = r.hips.position.y - .03; r.hips.position.y = L(r.hips.position.y, hy, s); r.hips.position.z = L(r.hips.position.z, .06, s);
    for (const leg of r.legs) {                          // the feet well out in front on the floor (a high seat: on the step half a metre down), knees a little apart
      const t0 = leg.thigh.rotation.x, k0 = leg.knee.rotation.x, a0 = leg.ankle.rotation.x, ang = legIK(leg, ANK + (sy > .62 ? (sy - .5) / h : 0) - (hy - HIP_OFF), sy > .62 ? .4 : .5);
      leg.thigh.rotation.x = L(t0, leg.thigh.rotation.x, s); leg.knee.rotation.x = L(k0, leg.knee.rotation.x, s);
      leg.ankle.rotation.x = L(a0, -ang - .35, s); leg.thigh.rotation.z = L(leg.thigh.rotation.z, leg.side * .12, s);
    }
    r.torso.rotation.x = L(r.torso.rotation.x, -.3, s); r.head.rotation.x = L(r.head.rotation.x, .22 + .04 * Math.sin(t * .3 + ph), s);
    const back = Math.floor(ph * 7) % 3 === 2;            // one in three: hands behind the head
    for (const a of r.arms) back ? armTo(a, s, -2.7, -2.35, .75, .3) : armTo(a, s, -.55, -1.5, -.1, .15);
  } },
  // 0.84.9 (rec engineer B2): the stage. sing (at the mic stand), juggle (the balls are recCrewBalls'), bow, and address (the lectern)
  sing: { f(r, s, t, b, ph) {                            // both hands up on the mic, a sway with the song
    for (const a of r.arms) armTo(a, s, -1.25 + .06 * Math.sin(t * 1.7 + ph), -1.75, a.side * -.05, .2);
    r.torso.rotation.z = L(r.torso.rotation.z, .07 * Math.sin(t * 1.6 + ph), s); r.head.rotation.x = L(r.head.rotation.x, -.12 + .06 * Math.sin(t * 3.2), s);
  } },
  juggle: { f(r, s, t, b, ph) {                          // forearms out, the hands taking turns to toss, eyes up on the balls
    for (const a of r.arms) { const u = Math.sin(t * 2 * Math.PI * 1.1 + (a.side > 0 ? 0 : Math.PI)); armTo(a, s, -.8 - .22 * u, -1.05 + .2 * u, .14, -.2); }
    r.head.rotation.x = L(r.head.rotation.x, -.38, s);
  } },
  bow: { f(r, s, t, b, ph) {                             // a deep bow, one hand across the waist
    r.torso.rotation.x = L(r.torso.rotation.x, .85, s); r.head.rotation.x = L(r.head.rotation.x, .2, s);
    for (const a of r.arms) a.side > 0 ? armTo(a, s, -.35, -1.9, -.25, 0) : armTo(a, s, .15, -.2, .1, 0);
  } },
  address: { f(r, s, t, b, ph) {                         // hands on the lectern, a slow look round the room; now and then a hand opens out
    const g = pulse(t, 9, 2.4, ph * 9);
    for (const a of r.arms) a.side > 0 && g > 0 ? armTo(a, s, L(-.7, -1.15, g), L(-.55, -.9, g), L(.12, .55, g), -.3 * g) : armTo(a, s, -.7, -.55, .12, .1);
    r.head.rotation.y = L(r.head.rotation.y, .45 * Math.sin(t * .33 + ph * 6), s); r.head.rotation.x = L(r.head.rotation.x, -.05, s);
  } },
};
// climbing legs: the `side` foot steps up as q goes 0 to 1, the other pushes down; feet toward the wall
function recLegs(r, s, side, q) {
  const hy = r.hips.position.y;
  for (const leg of r.legs) {
    const k = leg.side === side ? q : 1 - q, t0 = leg.thigh.rotation.x, k0 = leg.knee.rotation.x, a0 = leg.ankle.rotation.x;
    const ang = legIK(leg, ANK + L(.02, .32, k) - (hy - HIP_OFF), L(.1, .2, k));
    leg.thigh.rotation.x = L(t0, leg.thigh.rotation.x, s); leg.knee.rotation.x = L(k0, leg.knee.rotation.x, s); leg.ankle.rotation.x = L(a0, -ang + .15, s);
    leg.thigh.rotation.z = L(leg.thigh.rotation.z, leg.side * .16, s);
  }
}
Object.assign(ACTS, REC_ACTS);
for (const a in REC_ACTS) CROWD_ANIMS.add(a);
function recRoot(o, root, t) {                           // the rec moves' whole-body part, each by its blend weight
  for (const key in o.k) { const A_ = ACTS[key]; if (A_ && A_.root && o.k[key] > .001) A_.root(o, root, ss(o.k[key]), t); }
}
// ---- the rec kit for you (0.81.0): playerKit('rec') or playerKit(null). Your Walker is rebuilt in the new clothes, and
// so is the stand-in if you're at a place. Not saved: a reload finds you in uniform. ----
function playerKit(k = null) {
  if ((PLAYER_SPEC.kit || null) === k) return false;
  for (const s of [PLAYER_SPEC, player.spec]) { if (k) s.kit = k; else delete s.kit; }
  const w = player, old = w.rig;
  w.obj.remove(old.root); old.root.traverse(o => { if (o.isMesh) o.geometry.dispose(); });
  w.rig = makeCharacter(w.spec); w.obj.add(w.rig.root); w.rig.root.traverse(o => { o.userData.walker = w; });
  w.propMeshes = []; w.propKey = ''; w.bodyProps = null;
  if (ACT && ACT.body) recBody(ACT);
  const grubby = !k && typeof uniformState === 'function' && uniformState() === 'grubby';
  if (typeof playerUniformTint === 'function' && (grubby || UNIFORM_MAT)) playerUniformTint(grubby ? 1 : 0);
  return true;
}
function recBody(A, extra) {                             // a new stand-in in your clothes now (plus extra: { socks: true }), where the old one was
  const b = A.body, nb = new FullPerson({ ...PLAYER_SPEC, ...extra }, 'you');
  nb.set({ x: A.x, y: A.y, z: A.z }, A.face, b ? b.pose : 'stand'); nb.rot = A.face;
  if (b) b.dispose(); A.body = nb;
}
// a towel over your shoulder after a swim: recTowel(mins) for that many ship minutes (the Walker's '+towel')
function recTowel(mins = 20) { player.towel = shipNow() + mins; }
// changing at a locker: the wardrobe's browse for two ship minutes, then into rec kit (or back; o.kit: 'rec' or null)
Object.assign(PLAYER_ACTS, { recChange: { mins: 2, pose: 'browse', title: 'Changing', until: A => {
  if (A.done < A.def.mins) return false;
  if (!A.o.changed) { A.o.changed = true; playerKit(A.o.kit !== undefined ? A.o.kit : PLAYER_SPEC.kit ? null : 'rec'); }
  return true;
} } });
// ---- the mover ----
const recXZ = p => ({ x: p[0] - OX, z: p[1] - OZ });
const recFace = f => typeof f === 'number' ? f * Math.PI / 180 : FACE_ANGLE[f] || 0;
function recGlide(A, x, z, sp, dt) {                     // toward x, z at sp m/s, facing the way; true when there
  const dx = x - A.x, dz = z - A.z, d = Math.hypot(dx, dz), st = sp * dt;
  if (d > 1e-4) A.face = Math.atan2(dx, dz);
  if (d <= st) { A.x = x; A.z = z; return true; }
  A.x += dx / d * st; A.z += dz / d * st; return false;
}
const recTimeUp = (A, n, count) => n ? count >= n : A.done >= A.def.mins;
const REC_MOVES = {
  swim(A, M, S, dt) {
    const P = M.path.map(recXZ); A.y = M.y || 0;
    if (!S.step) { S.step = 'in'; S.leg = 0; S.k = 0; }
    if (S.step === 'in') { if (recGlide(A, P[0].x, P[0].z, .6, dt)) { S.step = 'turn'; S.k = 0; S.f = Math.atan2(P[1].x - P[0].x, P[1].z - P[0].z); } return 'tread'; }
    if (S.step === 'turn') { A.face = S.f; S.k += dt; if (S.k > 1.3) S.step = 'swim'; return 'tread'; }
    if (S.step === 'swim') {
      const a = P[S.leg % 2], b = P[1 - S.leg % 2];
      if (recGlide(A, b.x, b.z, M.speed || .75, dt)) {
        S.leg++; S.k = 0;
        if (recTimeUp(A, M.lengths, S.leg) && (M.lengths || S.leg % 2 === 0)) S.step = 'end';
        else { S.step = 'turn'; S.f = Math.atan2(a.x - b.x, a.z - b.z); }
      }
      return 'swim';
    }
    S.k += dt; if (S.k > 1) S.done = true; return 'tread';
  },
  tread(A, M, S, dt, t) {
    const p = recXZ(M.at); A.x = p.x; A.z = p.z; A.y = M.y || 0;
    if (S.f === undefined) S.f = M.face !== undefined ? recFace(M.face) : A.face;
    A.face = S.f + .5 * Math.sin(t * .15);
    if (A.done >= A.def.mins) S.done = true; return 'tread';
  },
  kayak(A, M, S, dt) {
    const P = M.path; A.y = M.y || 0;
    if (S.i === undefined) { S.i = 0; S.lap = 0; S.go = false; }
    const p = P[S.i], q = recXZ(p); A.body.fast = !!p[2];
    if (recGlide(A, q.x, q.z, S.go ? (p[2] ? 1.7 : 1.05) : .7, dt)) {
      if (S.go && S.i === 0) { S.lap++; if (recTimeUp(A, M.laps, S.lap)) { S.done = true; return 'kayak'; } }
      S.go = true; S.i = (S.i + 1) % P.length;
    }
    return 'kayak';
  },
  climb(A, M, S, dt, t) {
    const p = recXZ(M.at), f = recFace(M.face), top = M.top || 3.2;
    if (!S.step) { S.step = 'to'; S.k = 0; A.y = 0; }
    if (S.step === 'to') { if (!recGlide(A, p.x, p.z, .8, dt)) return 'walk'; S.step = 'up'; }
    A.x = p.x; A.z = p.z; A.face = f;
    let pose = 'climb';
    if (S.step === 'up') { A.y += .34 * dt * (.35 + .65 * Math.abs(Math.sin(t * .85 * Math.PI))); if (A.y >= top) { A.y = top; S.step = 'ring'; if (M.onRing) try { M.onRing(); } catch (e) { /* the room's */ } } }
    else if (S.step === 'ring') { pose = 'ring'; S.k += dt; if (S.k > 2.6) S.step = 'lower'; }
    else if (S.step === 'lower') { pose = 'lower'; A.y = Math.max(0, A.y - .6 * dt); if (!A.y) { S.step = 'off'; S.k = 0; } }
    else { pose = 'stand'; S.k += dt; if (S.k > .7) S.done = true; }
    recRope(A, p.x + Math.sin(f) * .2, top + 1.1, p.z + Math.cos(f) * .2, S.step !== 'off');
    return pose;
  },
  float(A, M, S, dt) {
    const c = recXZ(M.at), r = M.r !== undefined ? M.r : 1.2, top = M.top || 2.2;
    if (!S.t) { S.t = 0; S.f = A.face; if (A === ACT) recBody(A, { socks: true }); }
    const n = Math.floor(S.t / 5), u = (S.t % 5) / 5;     // one slow bounce every five seconds
    if (n >= 1 && u < dt / 5 + 1e-9 && recTimeUp(A, M.bounces, n)) { S.done = true; A.body.spin = 0; A.body.rig.star = 0; return 'float'; }
    S.t += dt;
    A.y = top * Math.sin(Math.PI * u) * (n === 0 ? ss(Math.min(1, S.t / 2)) : 1);
    const flip = n % 3 === 2;                            // every third bounce a slow somersault, otherwise a star at the top
    A.body.spin = flip ? 2 * Math.PI * ss(u) : 0; A.body.rig.star = flip ? 0 : Math.pow(Math.sin(Math.PI * u), 6);
    const tx = c.x + r * Math.sin(S.t * .23), tz = c.z + r * .7 * Math.sin(S.t * .17 + 1);
    A.x += (tx - A.x) * Math.min(1, dt * .8); A.z += (tz - A.z) * Math.min(1, dt * .8); A.face = S.f + S.t * .22;
    return 'float';
  },
};
function recMoveStep(A, dt, t) {
  const M = A.o.move, fn = M && REC_MOVES[M.kind]; if (!fn || !A.body) return null;
  const S = A.mv || (A.mv = {});
  if (S.done) return M.kind === 'climb' ? 'stand' : M.kind === 'kayak' ? 'kayak' : M.kind === 'swim' || M.kind === 'tread' ? 'tread' : 'stand';
  return fn(A, M, S, dt, t);
}
// the belay line, from the harness up to the top anchor (world x, y, z): one thin mesh on the stand-in's root (so it
// goes when the stand-in does), its own geometry and a shared material made the first time
let REC_ROPE_MAT = null; const _ropeA = new THREE.Vector3(), _ropeB = new THREE.Vector3(), _ropeU = new THREE.Vector3(0, 1, 0);
function recRope(A, ax, ay, az, on) {
  const root = A.body.rig.root; if (!A.body.full) return;   // a crowd body's root isn't in the scene (phase 2: the crew's own line)
  if (!A.rope) {
    A.rope = new THREE.Mesh(cylG(1, 1, 1, 6).clone(), REC_ROPE_MAT || (REC_ROPE_MAT = new THREE.MeshStandardMaterial({ color: col('#3a7bd5'), roughness: .7 })));
    A.rope.castShadow = true; root.add(A.rope);
  }
  A.rope.visible = on; if (!on) return;
  root.updateMatrixWorld(true);
  _ropeA.set(0, .71, .19); _ropeB.set(ax, ay, az); root.worldToLocal(_ropeB);   // the belay loop, in the root's own units
  const d = _ropeB.clone().sub(_ropeA), len = d.length(), rr = .016 / A.body.h;
  A.rope.position.copy(_ropeA).addScaledVector(d, .5); A.rope.quaternion.setFromUnitVectors(_ropeU, d.normalize()); A.rope.scale.set(rr, len, rr);
}
// ---- the crew's moves (0.84.6, rec engineer B). Whoever is settled at a place with `move` (the mover's specs above, deck
// coordinates) does it as an endless loop, no counts, from their own clock (a.mt: real seconds since they settled there;
// the first 1.5 s glide from the place's spot to the move's start). The agent stays at the spot (its tiles, getting up);
// only the body moves. The place's fields (section 10's placeSpot passes `move` on as spot.mv):
//   swim  { path: [a, b], y, speed?, phase? }  lengths, a tread at each end    tread { at, y, face }
//   kayak { path: REC_LOOP, y, phase? }        the loop at the player's speeds  float { at, r, top }
//   climb { at, face, top, rest? }  up, the bell, lowered, `rest` s at the foot (4): a belay line while on (two at once)
//   fan   { slump? }  at a seat or standing: watching, and the room's cheers, claps and groans together (one shared clock)
//   kit: 'rec' (swim, tread and kayak's default), 'socks' (float's), 'rec socks' or '' (in uniform): a new body for it
// phase: 0-1 of the loop, so two on one loop or lane are apart. A seat with anim: 'slump' and no move sits back, legs out.
// Nothing here calls R(); a place with no `move` never comes here.
const REC_KITS = { swim: 'rec', tread: 'rec', kayak: 'rec', float: 'socks' };
const _rcp = { x: 0, y: 0, z: 0, f: 0 }, _rcC = new WeakMap(), REC_CLIMBERS = [{}, {}]; let REC_CREW_ROPES = null, REC_CLIMB_N = 0;
const recCrewC = M => _rcC.get(M) || (_rcC.set(M, { P: (M.path || [M.at || [0, 0]]).map(recXZ) }), _rcC.get(M));   // the move's points in world units, once
const recMix = x => { x = Math.imul(x ^ x >>> 15, 2246822507); x = Math.imul(x ^ x >>> 13, 3266489909); return (x ^ x >>> 16) >>> 0; };
function recCrewSet(a, dt) {                             // false: not a move (the agent sets the body as usual)
  const M = a.settled && a.spot ? a.spot.mv : null, want = M ? (M.kit !== undefined ? M.kit : REC_KITS[M.kind] || '') : '';
  if (want !== (a.rkH === a.h ? a.rk : '')) recCrewKit(a, want); else if (a.rkH !== a.h) a.rk = '';   // a new body since (crewDetail's): in uniform
  const fn = M && REC_CREW[M.kind]; if (!fn) return false;
  if (a.mtId !== a.spot.id) { a.mtId = a.spot.id; a.mt = 0; a.fs = idHash(a.p.id); }
  a.mt += dt; const o = _rcp; o.x = a.x; o.y = a.y; o.z = a.z; o.f = a.face;
  const pose = fn(a, M, a.mt, o, recCrewC(M));
  if (a.mt < 1.5) { const k = ss(a.mt / 1.5); o.x = L(a.x, o.x, k); o.z = L(a.z, o.z, k); }
  a.h.set(o, o.f, pose); return true;
}
function recCrewKit(a, k) {                              // into rec kit or grip socks and back: a new body of the same kind
  const spec = Object.assign({}, rosterSpec(a.p)); if (/rec/.test(k)) spec.kit = 'rec'; if (/socks/.test(k)) spec.socks = true;
  const full = !!a.h.full; a.remove(); a.h = full ? new FullPerson(spec, a.p.id) : crowd.add(spec); a.rk = k; a.rkH = a.h;
}
const REC_CREW = {
  swim(a, M, T, o, C) {                                  // tread at a (facing b), swim to b, tread, swim back
    const A = C.P[0], B = C.P[1], ts = Math.hypot(B.x - A.x, B.z - A.z) / (M.speed || .75), tt = 2 + a.fs % 15 / 10, per = 2 * (ts + tt);
    let u = (T + (M.phase || 0) * per) % per; const bk = u >= ts + tt; if (bk) u -= ts + tt;
    const p = bk ? B : A, q = bk ? A : B, sw = u >= tt, k = sw ? (u - tt) / ts : 0;
    o.x = L(p.x, q.x, k); o.z = L(p.z, q.z, k); o.y = M.y || 0; o.f = Math.atan2(q.x - p.x, q.z - p.z);
    return sw ? 'swim' : 'tread';
  },
  tread(a, M, T, o, C) { o.x = C.P[0].x; o.z = C.P[0].z; o.y = M.y || 0; o.f = (M.face !== undefined ? recFace(M.face) : a.spot.face) + .5 * Math.sin(T * .15 + a.fs % 7); return 'tread'; },
  kayak(a, M, T, o, C) {                                 // round the loop at 1.05 m/s, 1.7 on the white water (a point's third number)
    const P = C.P, n = P.length;
    if (!C.T) { C.T = []; let t = 0; for (let i = 0; i < n; i++) { const q = P[(i + 1) % n]; t += Math.hypot(q.x - P[i].x, q.z - P[i].z) / (M.path[(i + 1) % n][2] ? 1.7 : 1.05); C.T.push(t); } }
    const tot = C.T[n - 1]; let u = (T + (M.phase || 0) * tot) % tot, i = 0; while (i < n - 1 && C.T[i] < u) i++;
    const t0 = i ? C.T[i - 1] : 0, p = P[i], q = P[(i + 1) % n], k = (u - t0) / (C.T[i] - t0 || 1);
    o.x = L(p.x, q.x, k); o.z = L(p.z, q.z, k); o.y = M.y || 0; o.f = Math.atan2(q.x - p.x, q.z - p.z); a.h.fast = !!M.path[(i + 1) % n][2];
    return 'kayak';
  },
  climb(a, M, T, o, C) {                                 // a rest at the foot, up (in bursts, as yours), the bell, lowered
    const top = M.top || 3.2, w = .85 * Math.PI, Y = t => .34 * (.35 * t + .65 * (2 * Math.floor(w * t / Math.PI) + 1 - Math.cos(w * t % Math.PI)) / w);
    if (!C.tu) { let t = 0; while (Y(t) < top) t += .05; C.tu = t; C.ys = top / Y(t); }
    const rest = M.rest !== undefined ? M.rest : 4, tl = top / .6, per = rest + C.tu + 2.6 + tl, u = (T + (M.phase || 0) * per) % per, f = recFace(M.face), P = C.P[0];
    o.f = f; o.x = P.x; o.z = P.z; let pose;
    if (u < rest) { o.y = 0; pose = 'stand'; }
    else if (u < rest + C.tu) { o.y = Math.min(top, Y(u - rest) * C.ys); pose = 'climb'; }
    else if (u < rest + C.tu + 2.6) { o.y = top; pose = 'ring'; }
    else { o.y = Math.max(0, top - .6 * (u - rest - C.tu - 2.6)); pose = 'lower'; }
    if (u >= rest && REC_CLIMB_N < 2) {                  // on the line: the anchor above the route
      if (!REC_CREW_ROPES) REC_CREW_ROPES = [0, 1].map(() => {
        const m = new THREE.Mesh(cylG(1, 1, 1, 6).clone(), REC_ROPE_MAT || (REC_ROPE_MAT = new THREE.MeshStandardMaterial({ color: col('#3a7bd5'), roughness: .7 })));
        m.castShadow = true; m.visible = false; m.raycast = () => {}; scene.add(m); return m;
      });
      const c = REC_CLIMBERS[REC_CLIMB_N++]; c.h = a.h; c.x = P.x + Math.sin(f) * .2; c.y = top + 1.1; c.z = P.z + Math.cos(f) * .2;
    }
    return pose;
  },
  float(a, M, T, o, C) {                                 // a slow bounce every five seconds; every third a somersault, else a star at the top
    const r = M.r !== undefined ? M.r : 1.2, top = M.top || 2.2, n = Math.floor(T / 5), u = T % 5 / 5, flip = n % 3 === 2, c = C.P[0];
    o.y = top * Math.sin(Math.PI * u) * (n === 0 ? ss(Math.min(1, T / 2)) : 1);
    a.h.spin = flip ? 2 * Math.PI * ss(u) : 0; a.h.rig.star = flip ? 0 : Math.pow(Math.sin(Math.PI * u), 6);
    o.x = c.x + r * Math.sin(T * .23 + a.fs % 5); o.z = c.z + r * .7 * Math.sin(T * .17 + 1 + a.fs % 3); o.f = a.spot.face + T * .22;
    return 'float';
  },
  // 0.84.9 (rec engineer B2): on the stage. perform { act: 'sing' | 'juggle' | 'piano' | 'bow', len?: seconds } does the act,
  // then a bow for its last 3 s and round again (piano: a seated place, pose 'sit'; bows standing up from the bench, no).
  // address {} (the lectern: the Captain, the chief or a Wren talk's speaker). Both stay at the place, as it faces.
  perform(a, M, T, o) {
    const act = M.act || 'sing', per = (M.len || 40) + 3, u = (T + a.fs % 11) % per;
    if (act === 'piano') return 'sit:play';
    if (u >= per - 3) return 'bow';
    if (act === 'juggle' && REC_JUGGLE.n < 1) { REC_JUGGLE.h = a.h; REC_JUGGLE.t = T; REC_JUGGLE.n = 1; }
    return act;
  },
  address() { return 'address'; },
  fan(a, M, T, o) {                                      // watching; every six seconds the room may cheer a point or groan a miss, each a moment late
    const ct = clock.elapsedTime - a.fs % 7 * .09, n = Math.floor(ct / 6), m = recMix(n * 7919 + 13) % 20, me = recMix(n * 31 + a.fs) % 10;
    const sat = a.spot.pose === 'sit', still = sat ? (M.slump ? 'sit:slump' : 'sit') : 'stand';
    if (ct / 6 - n > .55 || m < 9 || me < 2) return still;
    const x = m < 13 ? 'groan' : me < 6 ? 'cheer' : 'clap'; return sat ? 'sit:' + x : x;
  },
};
// 0.84.9: the juggler's three balls, one mesh of three instances, made at the first juggle; a cascade in front of the chest
const REC_JUGGLE = { m: null, h: null, t: 0, n: 0 }, _jq = new THREE.Object3D(), _jv = new THREE.Vector3();
function recCrewBalls() {
  const J = REC_JUGGLE, on = J.n > 0 && crowd.visible && J.h && J.h.rig;
  if (!J.m && on) {
    J.m = new THREE.InstancedMesh(new THREE.SphereGeometry(.06, 10, 8), new THREE.MeshStandardMaterial({ roughness: .5 }), 3);
    ['#ff5a4f', '#ffd23a', '#4fc3ff'].forEach((c, i) => J.m.setColorAt(i, col(c))); J.m.castShadow = true; J.m.raycast = () => {}; J.m.frustumCulled = false; scene.add(J.m);
  }
  if (J.m) J.m.visible = !!on;
  if (on) {
    for (let i = 0; i < 3; i++) {                        // ball i: up from one hand, across, down into the other; each a third of a beat apart
      const u = (J.t * 1.1 + i / 3) % 1, k = u < .5 ? u * 2 : (u - .5) * 2, side = (Math.floor(J.t * 1.1 + i / 3) + (u < .5 ? 0 : 1)) % 2 ? 1 : -1;
      _jv.set(side * L(-.16, .16, k), .5 + .4 * Math.sin(Math.PI * k), .34).applyMatrix4(J.h.rig.root.matrixWorld); _jv.y += Math.max(0, J.h.pos.y - J.h.rig.root.position.y);   // on a stage the root stays on the floor (the legs stand on it)
      _jq.position.copy(_jv); _jq.updateMatrix(); J.m.setMatrixAt(i, _jq.matrix);
    }
    J.m.instanceMatrix.needsUpdate = true;
  }
  J.n = 0;
}
function recCrewRopes() {                                // after the crowd is posed (the main loop): harness to anchor, hidden when nobody's on
  for (let i = 0; i < 2; i++) {
    const m = REC_CREW_ROPES[i], c = REC_CLIMBERS[i], on = i < REC_CLIMB_N && crowd.visible && !!c.h.rig; m.visible = on; if (!on) continue;
    _ropeA.set(0, .71, .19).applyMatrix4(c.h.rig.root.matrixWorld); _ropeB.set(c.x, c.y, c.z).sub(_ropeA);
    const len = _ropeB.length(); m.position.copy(_ropeA).addScaledVector(_ropeB, .5); m.quaternion.setFromUnitVectors(_ropeU, _ropeB.normalize()); m.scale.set(.016, len, .016);
  }
  REC_CLIMB_N = 0;
}
// 0.84.8 (rec engineer B2): the auditorium's show. RA's traditions engine calls recShow(state) whenever the show changes
// (and may call it every tick: same state, no work): null (no show), 'film' (the screen down and lit, the house lights
// well down), 'talk' (a Wren talk: the lectern's pool, the house lights a little down), 'allhands' (the same, a touch
// brighter on the stage), 'talent' (all three pools, the house lights down). Looks only: nothing saved, nothing
// random. The house lights dim only while you're in the auditorium; arriving mid-show, the screen and pools are set at once.
// (REC_POOLS, REC_SHOWS and REC_SHOW are with REC_DECK at the top: the deck's build reads them)
function recShow(state) {
  const s = REC_SHOWS[state] ? state : null; if (s === REC_SHOW.state) return;
  REC_SHOW.state = s; recPoolsSet();
}
function recPoolsSet() {                                 // each pool's colour from the show (warm white; talent night's centre a little pink)
  const m = REC_SHOW.pools; if (!m || !m.parent) return;
  const S = REC_SHOWS[REC_SHOW.state], a = m.geometry.attributes.color, tint = [[1, .9, .7], [1, .82, .86], [.85, .88, 1]];
  for (let k = 0; k < REC_POOLS.length; k++) { const b = S ? S.pools[k] * 1.1 : 0; for (let v = 0; v < 4; v++) a.setXYZ(k * 4 + v, tint[k][0] * b, tint[k][1] * b, tint[k][2] * b); }
  a.needsUpdate = true; m.visible = !!S && S.pools.some(x => x > 0);
  if (REC_SHOW.ring) REC_SHOW.ring.visible = REC_SHOW.state === 'talk';   // 0.84.12: the talk's chairs and stool; the mic put aside
  if (REC_SHOW.mic) REC_SHOW.mic.visible = REC_SHOW.state !== 'talk';
}
const _recFilm = [col('#3a5b8c'), col('#c98a4a'), col('#5c8f6a'), col('#d9d2c4')], _recCloth = col('#e8e6df');   // the film's light on the screen: a slow drift through a few scenes' colours
function recShowTick(dt, t) {
  const S = REC_SHOWS[REC_SHOW.state], here = deckDef && deckDef.num === 7, ease = Math.min(1, dt * 1.2);
  const scr = S ? S.scr : 0, dim = S && here && lastRoom === 'A' ? S.dim : 0;
  REC_SHOW.scr = here ? (Math.abs(scr - REC_SHOW.scr) < .002 ? scr : REC_SHOW.scr + Math.sign(scr - REC_SHOW.scr) * Math.min(Math.abs(scr - REC_SHOW.scr), dt * .25)) : scr;   // the screen unrolls in about 4 s
  REC_SHOW.dim = Math.abs(dim - REC_SHOW.dim) < .002 ? dim : REC_SHOW.dim + (dim - REC_SHOW.dim) * ease;
  const p = here && REC_SHOW.piv; if (!p || !p.parent) return;
  p.scale.y = Math.max(.001, REC_SHOW.scr); p.visible = REC_SHOW.scr > .002;
  if (p.visible && RK && RK.film) {
    const lit = REC_SHOW.state === 'film' && REC_SHOW.scr > .98, k = (t * .05) % _recFilm.length, i = Math.floor(k), f = k - i;
    if (lit) RK.film.color.copy(_recFilm[i]).lerp(_recFilm[(i + 1) % _recFilm.length], f * f * (3 - 2 * f)).multiplyScalar(.75 + .1 * Math.sin(t * 2.3)); else RK.film.color.copy(_recCloth);
  }
}
function crewDetail() {                                  // who gets a full rig: the nearest story crew to you
  const pp = player.obj.position;
  const near = DECK_CREW.filter(a => a.p.story).map(a => [a, Math.hypot(a.x - pp.x, a.z - pp.z)])
    .filter(([a, d]) => d < (a.h.full ? FULL_FAR : FULL_NEAR)).sort((m, n) => m[1] - n[1]).slice(0, FULL_MAX).map(m => m[0]);
  for (const a of DECK_CREW) {
    const want = near.includes(a);
    if (want === !!a.h.full) continue;
    a.remove(); a.h = want ? new FullPerson(rosterSpec(a.p), a.p.id) : crowd.add(rosterSpec(a.p));
    a.h.set({ x: a.x, y: a.y, z: a.z }, a.face, heldPose(a));
  }
}
// placeBusy(id): is someone settled at that place on this deck? A Set rebuilt once a frame, so it's a cheap lookup
// for kit that animates while in use (the treadmill belts, the rower). PLAYER_PLACE is the player's own place id
// when the player is using one (section 15 sets it), or null.
const BUSY = new Set(); let PLAYER_PLACE = null;
const placeBusy = id => BUSY.has(id) || PLAYER_PLACE === id;
let crewCheckT = 0;
function deckCrewClear() { for (const a of DECK_CREW) a.remove(); DECK_CREW.length = 0; BUSY.clear(); LINE.length = 0; CREW_HELD.clear(); CREW_WAY.clear(); }
// everyone whereIs puts on this deck, mid-activity: at their place, partway there, or still in the lift
function deckCrewFill() {
  deckCrewClear();
  PLACE_OF = new Map((deckDef.places || []).map(p => [p.id, p])); SPOT_OF = new Map();
  const now = shipNow(), N = deckDef.num;
  for (const p of schedPeople()) { const w = whereIs(p, now); if (w.deck === N) crewArrive(p, w, now, true); }
  lineCatchUp(now);
}
// a mid fill on the way to the servery line (0.26.34, player engineer 4: a scene started at 07:12 had 21 in the line,
// all set off at once): when each would have reached the line, walking from where they set off; then the line played
// forward to now, a serving at a time. Served: on to their seat, partway; still waiting: in their place in the line;
// not there yet: partway along. So a deck entered mid-meal looks like one watched from the start
const LINE_CATCH = [];
function lineCatchUp(now) {
  const L = LINE_CATCH.splice(0); if (!L.length) return;
  const serve = typeof galleyServeMins === 'function' ? galleyServeMins(now) : LINE_SERVE;
  const rows = L.map(([a, w]) => {
    let s = w; for (let k = 0; k < 4; k++) { const pv = whereIs(a.p, s.from - .01); if (!pv || !lineSeg(pv) || pv.act !== w.act) break; s = pv; }   // when they set off for it
    a.retarget(lineSpotId(0));
    return { a, w, off: s.from, arrive: s.from + a.path.length / CREW_SPEED * SHIP_RATE };
  }).sort((x, y) => x.arrive - y.arrive || (x.a.p.id < y.a.p.id ? -1 : 1));
  let free = -Infinity;
  for (const { a, w, off, arrive } of rows) {
    a.meal = { key: w.act + Math.floor(w.from / 1440), served: false, tray: false };
    if (arrive > now) {                                  // still walking
      const done = Math.floor((now - off) / SHIP_RATE * CREW_SPEED);
      if (done > 0 && done < a.path.length) { const c = cellPos(...a.path[done - 1]); a.x = c.x; a.z = c.z; a.path = a.path.slice(done); }
      continue;
    }
    const t = (free = Math.max(arrive, free) + serve); LINE_LOG.joined++;
    if (t <= now) {                                      // served already: from the counter towards their seat
      const c = placeSpot(lineSpotId(0)); a.served(w, t); a.path = []; a.spot = null; a.settled = false; a.goalId = undefined;
      if (c) { a.x = c.x; a.z = c.z; }
      const goal = a.meal.next; if (!goal || goal === '@lift') continue;
      a.retarget(goal); const sp = placeSpot(goal), done = Math.floor((now - t) / SHIP_RATE * CREW_SPEED);
      if (sp && a.path.length && done >= a.path.length) { if (spotTaken(a, goal)) { arriveNear(a); continue; } a.path = []; a.x = sp.x; a.z = sp.z; a.settled = true; a.pose = crewPose(a); a.face = sp.face; a.y = sp.y; }
      else if (done > 0 && done < a.path.length) { const q = cellPos(...a.path[done - 1]); a.x = q.x; a.z = q.z; a.path = a.path.slice(done); }
      continue;
    }
    const k = LINE.length, id = lineSpotId(k), sp = id && placeSpot(id);   // waiting: their place in the line
    LINE.push(a.p.id); a.lineAt = now; LINE_LOG.long = Math.max(LINE_LOG.long, LINE.length);
    if (sp) { a.retarget(id); a.path = []; a.x = sp.x; a.z = sp.z; a.settled = true; a.face = sp.face; a.pose = 'stand'; }
  }
}
// arriving part way (crewArrive, lineCatchUp) never sits anyone in a place someone's still settled in (0.36.87: day 100's
// Founding Day walk onto Deck 3 during the Spice shelf supper seated two at 3-mess-12): they stop on its walk-to tile instead
const spotTaken = (a, id) => !!id && (PLAYER_PLACE === id || DECK_CREW.some(o => o !== a && o.settled && o.spot && o.spot.id === id));
function arriveNear(a) { const c = cellPos(...a.path[a.path.length - 1]); a.x = c.x; a.z = c.z; a.path = a.path.slice(-1); }
function crewArrive(p, w, now, mid) {
  const N = deckDef.num, lift = liftTiles();
  if (w.visit) { DECK_CREW.push(new CrewAgent(p, lift.length ? lift[idHash(p.id) % lift.length] : nearestOpen(LIFT_AT[0], LIFT_AT[1], null))); return; }   // a visitor comes by lift
  if (w.escort) {                                        // the escort comes with you: out of the lift nearest you (waiting at a place: already there)
    const sp = w.escort.mode === 'wait' && w.placeId && placeSpot(w.placeId), wt = w.escort.mode === 'wait' && w.escort.to && Array.isArray(w.escort.to.tile) ? w.escort.to.tile : null;
    if (sp || wt) { DECK_CREW.push(new CrewAgent(p, sp ? sp.walk : wt)); return; }
    const pp = player.obj.position, near = lift.length ? lift.slice().sort((a, b) => cellPos(...a).distanceTo(pp) - cellPos(...b).distanceTo(pp))[0] : nearestOpen(pp.x, pp.z, null);
    DECK_CREW.push(new CrewAgent(p, near)); return;
  }
  if (w.act === 'commute') {                             // riding in: step out of the car when the ride's done
    if (now < w.until - .5) return;
    const a = new CrewAgent(p, lift.length ? lift[idHash(p.id) % lift.length] : nearestOpen(LIFT_AT[0], LIFT_AT[1], null)); DECK_CREW.push(a); return;
  }
  const spot = w.placeId && placeSpot(w.placeId);
  const prev = whereIs(p, w.from - .01);
  const prevSpot = prev && prev.deck === N && prev.placeId && placeSpot(prev.placeId);
  const start = prevSpot ? prevSpot.walk : lift.length ? lift[idHash(p.id) % lift.length] : nearestOpen(LIFT_AT[0], LIFT_AT[1], null);
  const a = new CrewAgent(p, start); DECK_CREW.push(a);
  if (mid && N === 3 && lineSeg(w) && (w.act === 'breakfast' || w.act === 'dinner')) { LINE_CATCH.push([a, w]); return; }   // placed by lineCatchUp, in line order
  a.retarget(w.placeId || null);
  if (!mid || !spot || !a.path.length) return;
  const done = Math.floor((now - w.from) / SHIP_RATE * CREW_SPEED);   // tiles walked since they set off
  if (done >= a.path.length && spotTaken(a, w.placeId)) arriveNear(a);   // someone's still in it: to its walk-to tile, and the next frame finds them another (elsewhere)
  else if (done >= a.path.length) { a.path = []; a.x = spot.x; a.z = spot.z; a.settled = true; a.tag = w.tag || null; a.pose = crewPose(a); a.face = spot.face; a.y = spot.y; }
  else if (done > 0) { const c = cellPos(...a.path[done - 1]); a.x = c.x; a.z = c.z; a.path = a.path.slice(done); }
}
// once a frame from the main loop: everyone moves; now and then, anyone due on this deck who isn't here yet arrives
function updateDeckCrew(dt) {
  const now = shipNow(), N = deckDef.num;
  lineTick(dt, now);
  queueTick(dt, now);                                    // the booth and shower lines (0.71.4)
  for (let i = DECK_CREW.length - 1; i >= 0; i--) if (!DECK_CREW[i].update(dt, now, N)) { DECK_CREW[i].remove(); DECK_CREW.splice(i, 1); }
  for (let i = 0; i < DECK_CREW.length; i++) { const a = DECK_CREW[i]; if (a.h.full) { a.h.update(dt, clock.elapsedTime); a.h.rig.root.visible = crowd.visible; } }   // indexed: no iterator a frame (0.26.40)
  BUSY.clear(); for (let i = 0; i < DECK_CREW.length; i++) { const a = DECK_CREW[i]; if (a.settled && a.spot) BUSY.add(a.spot.id); }
  PLAYER_PLACE = typeof playerHolds === 'function' ? playerHolds() : null;
  if ((crewCheckT -= dt) > 0) return;
  crewCheckT = .25;
  crewDetail();
  const here = new Set(DECK_CREW.map(a => a.p.id));
  for (const p of schedPeople()) if (!here.has(p.id)) { const w = whereIs(p, now); if (w.deck === N) crewArrive(p, w, now, false); }
}
// doors open for crew walking through them; a 'closed' one only for those whose rooms are behind it
function crewNearDoor(d) {
  const r = 1.15 + (d.span - SEG) / 2;
  if (!d.rooms) d.rooms = edgeTiles(d.e.key).map(c => roomAt(...c));
  // every door, every frame: plain loops, no closures (the performance engineer's garbage count, 0.26.40)
  const R = d.rooms;
  for (let i = 0; i < DECK_CREW.length; i++) {
    const a = DECK_CREW[i];
    if (a.settled || Math.abs(a.x - d.cx) > r || Math.abs(a.z - d.cz) > r || Math.hypot(a.x - d.cx, a.z - d.cz) > r) continue;
    if (d.passable) return true;
    for (let k = 0; k < R.length; k++) if (a.rooms.has(R[k])) return true;
  }
  if (d.e.type === 'closed') {                           // an invitation or summons: the door opens for you (you near it first: the cheap test)
    const p = player.obj.position;
    if (Math.hypot(p.x - d.cx, p.z - d.cz) < r) for (let k = 0; k < R.length; k++) if (doorOpenFor(R[k], 'player')) return true;
  }
  return false;
}
// a tap on someone: the nearest crew member whose body is under the finger, by screen distance
function crewAtScreen(cx, cy) {
  if (!crowd.visible) return null;
  let best = null, bd = 26 * Math.max(.8, camera.zoom);
  const mine = PLACE_OF.get(playerBed()), myBunk = mine && placeSpot(mine.id);   // a tap on your own bunk is for you,
  for (const a of DECK_CREW) for (const hy of (bp => bp === 'lie' && myBunk && Math.hypot(a.x - myBunk.x, a.z - myBunk.z) < .6 ? [] :   // not your bunkmate below
    bp === 'lie' ? [.15] : bp === 'sit' ? [.5, .9] : [.5, 1.0, 1.4])(a.settled && a.spot ? a.spot.pose : a.pose)) {
    _cp.set(a.x, a.y + hy, a.z).project(camera);
    const d = Math.hypot((_cp.x + 1) / 2 * innerWidth - cx, (1 - _cp.y) / 2 * innerHeight - cy);
    if (d < bd) { bd = d; best = a; }
  }
  return best;
}
function tapCrew(cx, cy) {
  const a = crewAtScreen(cx, cy); if (!a) return false;
  if (typeof introTap === 'function' && introTap(a.p)) return true;   // section 21: the arrival evening's tap-to-ask (0.26.31)
  if (typeof tradJoinTap === 'function' && tradJoinTap(a)) return true;   // section 18: tap someone at a tradition to join in (0.70.0)
  a.talking = 6; player.stop(); player.face = Math.atan2(a.x - player.obj.position.x, a.z - player.obj.position.z);
  if (typeof chatOpen === 'function' && chatOpen(a.p)) return true;   // section 20: the chat card
  const f = crewFeeling(a.p, shipNow());               // section 14: "Tomas looks tired"
  const el = typeof eventLine === 'function' ? eventLine(a.p, shipNow()) : null;   // section 18: "Coming to the quiz tonight?"
  toast(a.p.name, a.p.role + '. ' + (f ? f + ' ' : '') + (el ? '"' + el + '"' : a.p.bio));
  if (typeof playerChat === 'function') playerChat(a.p);  // section 15: chatting raises social
  return true;
}
SIM_ADVANCE.push(() => { if (typeof deckDef !== 'undefined' && deckDef) deckCrewFill(); });   // after a sleep, everyone where they now are
deckCrewFill();

