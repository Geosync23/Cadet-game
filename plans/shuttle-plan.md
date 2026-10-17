# The Tern you can walk inside (sketch for review)

The deck architect (seat 8), 2026-10-17, for the user's playtest note: *a new game starts with you inside the shuttle; then the ramp opens and you walk out.* The onboarding engineer (session_01KaHzfqSqF8B4bkNFrH1tsx) owns the arrival scene. This page is only the shuttle and its ramp. Nothing is built until the lead (for the user) agrees it.

## Why the Tern has to change

Today's Tern (kit `shuttle`, Deck 5 shuttle bay, room `S`) is a solid prop: 2.6 m wide, 4.6 m long, floor at 0.5 m and roof at 1.88 m. That leaves about 1.4 m inside, so nobody can stand up in it, and its tiles are blocked. To be walked through it needs a real cabin.

## The new Tern (proposal)

- **Size:** 3 tiles wide (2.8 m) × 6 tiles long (5.8 m), nose to the bay doors (west) as now, on the same pad. The cabin floor is at 0.25 m and the roof at 2.55 m (the deck is 2.8 m high). It stays a low, chunky shape, but taller.
- **Inside, one aisle:** a walkable aisle down the middle, four tiles long. There's a bench seat along each side (six seats, blocked tiles), the cockpit at the nose (two seats and a console, seen but not walked into), and the side door at the aisle's third tile.
- **The side ramp on the south side, as now,** so the greeting crowd and the Veyli farewell keep their layout: the ramp lowers from the door onto the bay floor (two tiles), facing the open south half of the bay and the haulway beyond.
- **Seeing inside:** while you're inside, the roof and the upper half of the hull hide (like a wall lowering), so you see yourself in the aisle. The rest of the time it's a whole shuttle. No fading and no new shaders.

```
        x:  1   2   3   4   5   6   7   8   9          (Deck 5, room S; north is up)
  row 5     .   .   .   .   .   .   .   .   .
  row 6     .  [c] [s] [s] [s] [s] [s]  .   .          c cockpit, s seats (blocked)
  row 7  bay[c]  a   a   a   a  [t]  .   .  -> haulway   a aisle (walkable), t tail locker
  row 8 doors  [c] [s] [s] (d) [s] [s]  .   .          d the door's well (walkable)
  row 9     .   .   .   .  R   .   .   .   .           R the ramp (walkable once down)
  row 10    .   .   .   .  R   .   .   .   .
  row 11    .   .   .   .  *   .   .   .   .           * the ramp's foot: the escort waits here
```

(Exact tiles get fixed when it's built. The pad and the bay doors stay where they are.)

## The ramp

- One hinged piece (a separate mesh, no merge), closed (upright, it is the door) or open (sloping to the floor, about 15°).
- **For the onboarding scene:** `ternRamp(open, secs)` opens (`true`) or closes (`false`) it over `secs` seconds (default 2.5). `ternRampOpen()` reads 0 to 1. While it's closed, the ramp tiles and the door well are blocked; once it's fully open they're walkable. Nothing calls it, so the ramp stays **open**, as today, unless the scene closes it.
- **Where you start:** place `5-tern-seat-1` (a seat by the door, type `event`, `tern`), plus `5-tern-aisle-1` (standing at the door, inside) and `5-tern-ramp-top` / `-foot` for the escort and the bag step (section 15's `bagGive` at the top of the ramp). `SHIP_START_ARRIVAL` (section 13, the sim engineer) would move from the ramp to the seat. That line is theirs.
- A soft sound and a light on the ramp are nice-to-haves, for whoever owns the sound.

## What else moves (all mine)

- The shuttle bay's gathering spots (`5-shuttle-bay-crowd-*`) under the bigger hull are regenerated, and the three leads move to the new ramp's foot. The spot count drops a little (about 124 → 110).
- `crate` props, floodlights and the bay doors stay.
- Crew plans: the Tern's places are event-tagged, so nobody uses them day to day (byte-identical, checked).
- Phones: the new hull reuses the Tern's materials (hull, cockpit glass, livery, steel). The roof is its own mesh so it can hide; about +2 draw calls on Deck 5 (175 by the lift today).

## Questions for the onboarding engineer and the lead

1. Do you start **sitting** (the scene stands you up when the ramp opens) or standing at the door?
2. Who opens the ramp: the scene after a beat (and after you type your name, in the shuttle), or you, with a tap on the door?
3. Should the ramp close again after you've walked off (the Tern "leaving" isn't in this sketch)?
4. Keep the side ramp (proposed: it keeps the greeting layout), or a tail ramp facing the haulway doors?
