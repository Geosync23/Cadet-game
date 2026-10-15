# Pillar 1 plan: the foundation of the Living Ship

Agreed with the user on 2026-10-15. Read with `design-doc.md` (sections "The living ship", "Crew simulation" and "The crew: 75 people"), `TEAM.md` and `DEV_NOTES.md`. This file is the shared plan every Pillar 1 session works from. If something here is wrong, tell the lead; don't work around it.

## What Pillar 1 delivers

All 75 crew living a varied daily routine across all six decks, on a 30-minute ship day. The game saves itself and resumes where you left off. Crowds stay inside a phone's budget.

Out of scope: ship systems, jobs, relationships, events (Pillars 2–4). The player's needs (hunger, rest, hygiene) only go as far as sleeping skips time to morning.

## The user's decisions

- **The ship day lasts 30 real minutes:** 0.8 ship minutes per real second.
- **The game starts on Day 1, a Monday, at 06:00,** with the player in Bunk 1 on Deck 4.
- **Saving:** automatic, in the browser, per device. The game resumes exactly where it was. The ship doesn't run while the game is closed.
- **Sleeping skips time to morning.**
- **All 75 crew from the start:** 60 on days, 15 on nights.
- **Names:** the crew designer picks names for the Works Chief and the six senior officers. They are provisional and can be changed later.
- **Reviews:** one check-in partway through (the roster and a crowd demo), and one at the end of the pillar.
- **No cap on parallel sessions.**

## Current state (build 0.14.0)

- `gameMin` runs at 1 ship minute per real second (a 24-minute day) and starts at 07:40.
- The Day/Night button toggles lighting and jumps the clock; nothing follows the time of day.
- 9 crew in `CREW` (section 9) wander by weighted room picks (`Walker.think`, section 10, a placeholder). Each has a full `makeCharacter` rig (section 8): fine for 9, far too many draw calls for 40.
- There is no save system.

## Workstreams

| # | Workstream | Owner | Section of the game file | Builds |
| --- | --- | --- | --- | --- |
| 1 | Time and saving | Sim engineer | new `// 13. SHIP TIME & SAVE` | 0.15.x |
| 2 | Crew roster | Crew designer (the deck planner, reassigned) | `// 9. CREW DATA` (replace) | 0.16.x |
| 3a | Places on Decks 4, 5 and 6 | Deck 6 architect | each deck's `DECKS[n]` | 0.17.x |
| 3b | Places on Decks 1 and 3 | Bridge architect | each deck's `DECKS[n]` | 0.18.x |
| 3c | Places on Deck 2 | Command architect | `DECKS[2]` | 0.19.x |
| 5 | Crowd rendering | Performance engineer | `// 8. CHARACTER KIT` plus new `// 8b. CROWD` | 0.20.x |
| 4 | Schedule engine and off-deck crew | Sim engineer | new `// 14. SCHEDULES` | 0.21.x |
| 6 | Crew on the deck, and the whole-day test | Sim engineer, with the others on call | section 10 `Walker.think` and new `day_check.py` | 0.22.x |

The lead merges onto `claude/ship-integration` and numbers each combined build 0.23.0, 0.24.0 and so on.

**Order:**
1. Workstreams 1, 2, 3 and 5 start together.
2. The sim engineer moves from 1 to 4 against the formats below, using stub data until 2 and 3 land.
3. Check-in with the user once 2 and 5 are done: the roster as a readable page, and a crowd demo of 40 crew in the mess hall.
4. Workstream 6, then the end-of-pillar review.

**Parallel-work rules, as overnight:**
- Each session edits only its own sections and its own rows in DEV_NOTES.
- Shared code changes are minimal, inert for anything that doesn't use them, and reported to the lead.
- Each session pushes to its own branch and reports after each push.
- `design-doc.md` is edited only on the lead branch: send the lead the wording.

## The shared formats

These are the interfaces between workstreams. The owner of each may refine the details, but must tell the lead and keep the other sessions' side working.

### Time (workstream 1)

```js
// SHIP.time survives deck changes and is saved.
SHIP.time = { day: 1, min: 360 };      // day 1 = Monday; min = ship minutes since midnight (06:00 = 360)
const SHIP_RATE = 1440 / 1800;         // ship minutes per real second (a 30-minute day)
shipNow()            // absolute ship minutes: (day - 1) * 1440 + min
weekday(day)         // 0 = Monday ... 6 = Sunday (ship-week names may come later)
sleepUntil(min)      // the player sleeps: time skips to `min` the next morning, and everyone's state is advanced (fast, no drawing)
```

- Lighting follows the clock: night from about 21:00 to 06:00, with a dusk and a dawn. The Day/Night button becomes a debug control or goes.
- Time never runs while the tab is hidden.

### Saving (workstream 1)

- **Where and what:** `localStorage` key `starship-cadet-save` holds JSON: `{ v: 1, build, time, player: { deck, tile, facing }, ship: {…}, crew: {…} }`.
- **When:** every ship hour, on deck change, and on `visibilitychange` (hidden) or `pagehide`.
- **Never fatal:** every read and write is in try/catch. With no storage, the game starts fresh.
- **New game:** a "New game" control clears the save.
- **Tests:** `?nosave` in the URL turns saving and loading off. `cadet_test.py` and `deck_check.py` must use it, so tests are never affected by a save.
- **Old saves:** a save whose `v` the build doesn't know is ignored, so the game starts fresh.

### The roster (workstream 2)

One entry per person, 75 in all, ranks as in `design-doc.md`: 1 Captain, 1 XO, 4 Chiefs, 6 Senior Officers, 16 Officers and 47 Juniors.

```js
{
  id: 'pell',                         // stable, lower-case; used by saves and schedules
  name: 'Pell Okafor', story: true,   // story: one of the ~10 hand-written crew
  rank: 'junior',                     // captain | xo | chief | senior | officer | junior
  dept: 'works',                      // works | watch | survey | infirmary | command | galley | helm | comms | ...
  role: 'Works technician',
  shift: 'day',                       // day | night (60 / 15); rota fields below decide days off
  rota: { offDays: [5, 6] },          // weekday numbers; staggered across the crew
  bed: '4-B2-3',                      // a bed place id (see Places)
  work: { deck: 5, place: 'work:works' },
  habits: ['early-riser', 'window-seat'],      // from a shared vocabulary the sim engineer reads
  traits: ['dry humour', 'restless'],
  looks: { skin, hair, hairColor, height, build, acc },   // as makeCharacter takes today
  bio: 'One line, as now.',
  life: ['A sister on Kesh who sends recipes.'],          // seeds for gossip later (Pillar 3)
  seed: 1234                          // per-person seed for daily variety
}
```

- **Story crew:** the existing 9 keep their current looks and bios, plus the Works Chief. Rina and Brennan get proper beds; Rina is in Bunk 2 with Pell, as the design doc says.
- **Generated crew:** made by a small generator from templates, but stored as fixed data in the file, so they never change between builds unless someone means them to.
- **Readable copy:** the designer also produces a readable roster page for the user's check-in (`plans/crew-roster.html`, in the style of the deck plans).

### Places (workstream 3)

Each deck definition gains a `places` list of every spot where someone does something:

```js
places: [
  { id: '4-B2-3', type: 'bed', at: [c, r], face: 'e', pose: 'lie', room: 'B' },
  { id: '3-mess-12', type: 'mess-seat', at: [c, r], face: 'n', pose: 'sit', room: 'M' },
  { id: '5-bench-1', type: 'work:works', at: [c, r], face: 's', pose: 'stand', room: 'w' },
  ...
]
```

- **`id` is unique ship-wide.** Beds are named so the roster can point at them:
  - Deck 4 bunks: `4-B<room>-<berth>`.
  - Deck 4 cabins: `4-01` to `4-24`.
  - Deck 2 rooms: `2-<room letter>`.
- **Types used in Pillar 1:**
  - `bed`
  - `shower`, `basin`, `toilet`
  - `mess-seat`, `servery-queue`, `grab-shelf`
  - `work:<dept>` for workstations: helm, ops, comms and the Works benches, galley stations, the infirmary, labs, the Watch office, engine control and the watch room
  - `gym`, `lounge-seat`, `garden`, `callhome`, `music`, `bench`, `common-room`, `laundry`
  - `lift-wait`
- **Poses:** `sit`, `stand`, `lie` or `work`.
- **Rules:**
  - A place tile must be walkable, or be a seat or bed that the walk-to tile beside it reaches.
  - `deck_check.py` gains a check that every place can be reached.
- **Counts:** every deck needs enough places for its busiest hour. For example, Deck 3's mess needs seats for about 40, and Deck 4 needs a bed for every crew member who sleeps there.

### Schedules (workstream 4)

```js
planDay(person, day)   // → [{ from, to, act, deck, type, placeId? }, ...] covering 24 hours, deterministic for (person.seed, day)
whereIs(person, t)     // → { deck, act, placeId, moving } at absolute ship minute t; works for any deck, drawn or not
```

- **Activities:** `sleep`, `wash`, `breakfast`, `dinner`, `work`, `leisure`, `gym`, `callhome`, `commute`, `off`.
- **Variety in layers, as in the design doc:** the rota and days off; the shape of each weekday (drills, inspections, the rest day); seeded jitter (waking 5–25 minutes either way, lingering at meals); habits; and choices weighted by need.
- **Meals:** breakfast 06:00–08:00 and dinner 17:00–20:30, plus the grab-and-go shelf.
- **Shifts:** days 08:00–17:00 and nights 21:00–06:00.
- **Commutes** use the lift, taking about 2 ship minutes. A crew member is "on" the destination deck after the ride.
- **Places:** a person never takes a place someone else holds. Beds are always the person's own.

### Crowd rendering (workstream 5)

- **Who uses what:**
  - The player and close crew may keep full rigs.
  - Everyone else is drawn through a crowd system: merged or instanced bodies, shared materials, a simpler figure at a distance, and poses for `walk`, `stand`, `sit`, `lie` and `work`.
- **The crowd system's interface** is roughly `crowd.add(spec)` and `crowd.remove(handle)`, with `handle.set(pos, face, pose, walkPhase)` and a `crowd.update(dt)` per frame.
- **Budget:** with 40 crew on Deck 3 at dinner, the whole frame stays under about 450 draw calls by the lift. Today's empty decks run 279–337.
- **Looks:** crew must still look like themselves: skin, hair, build, height and accessories.

### Crew on the deck (workstream 6)

- **On arriving at a deck,** everyone `whereIs` puts there appears at their place or on their way to it, mid-activity.
- **Crew follow their schedules:** walking to places, sitting, lying in their own beds, queueing at the servery, and arriving and leaving by lift.
- **The placeholder `think()` goes.**
- **`day_check.py`** (new) fast-forwards one ship day with `?nosave` and checks, deterministically:
  - everyone sleeps at least 6 hours in their own bed;
  - everyone eats twice;
  - everyone works their shift;
  - nobody is stuck for more than 10 ship minutes;
  - no two people share a place;
  - draw calls peak under budget on every deck;
  - the same seed gives the same day.

## Testing for the whole pillar

- **`cadet_test.py` compares Deck 4.** Workstreams 1, 5 and 6 change it on purpose: the clock and start time, how crew are drawn, and where crew are. Each of those turns must show the change is only the one meant, as in the guest-cabins turn, and the lead signs off a new baseline.
- **Decks without crew changes** stay pixel-identical with crew hidden.
- **`deck_check.py` must pass on all six decks every turn.** From workstream 3 on, it also checks that every place can be reached.

## Check-ins with the user

1. **Partway (after 2 and 5):** the roster page with all 75 people and their provisional names, and a playable crowd demo.
2. **End of Pillar 1:** a playable build where the ship runs through its days, plus a short report: what each crew member's week looks like, and the performance numbers.
