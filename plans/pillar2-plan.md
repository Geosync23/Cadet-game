# Pillar 2 plan: the ship comes alive, and needs looking after

Agreed with the user on 2026-10-15. Read with `design-doc.md` (above all "Ground rules", "Every room in use", "Food and cooking", "The clockwork", "The player"), `TEAM.md` and `DEV_NOTES.md`. Every Pillar 2 session works from this file. If something here is wrong, tell the lead; don't work around it.

## The ethos

**Everything functional, everything simulated.** Every room and every function aboard gets used, by the crew and by the player. The gym is for working out, the booths are for calling home, the store is for shopping, and the galley really cooks. Where full simulation isn't possible, get as close as we can. Never build a room that is only scenery.

## The user's decisions

- **Fitness gives no bonus.** Below a threshold you walk slower. The same goes for energy: too little sleep makes you slower too. Nothing else is punished (no fail state).
- **Needs show on your personal device.** The device will become the game's main interface. The user is still designing it, so Pillar 2 builds only a **plain placeholder** panel, which will be replaced. Keep the needs and jobs data separate from how they're shown.
- **No time controls.** There's no speed-up and no crew or systems panels. These are dropped from the plan.
- **No cap on parallel sessions.**
- **The deck architects stay on** for the utility rooms and new furniture.

## Starting point (build 0.25.2, `claude/ship-integration`)

- All 75 crew follow `planDay` and `whereIs` (section 14). They're drawn by the crowd (8b), and the 3 story crew nearest you get full rigs (section 10).
- Places exist on every deck, with types including `gym`, `callhome`, `shop`, `music`, `garden` and `laundry`.
- In those places today, crew only stand or sit. Nothing is animated, and nothing is consumed or used up.
- The player has no needs. Sleep (tap your bunk) is the only player action besides walking and tapping things.
- Sealed service rooms (air scrubbers, heating, utility closets, recycler, galley plant, irrigation, lab gas plant, cable crawl, Deck 6 junctions and crawlways) are empty and solid behind hatches.
- There are no machines, no wear and no jobs.

## Two halves

### Half A: the ship comes alive (starts now)

| # | Workstream | Owner | Section of the game file | Builds |
| --- | --- | --- | --- | --- |
| A1 | Every room in use: crew free time across the whole ship, crew needs, and activity choice | Sim engineer | 14 (schedules) and 10 (crew on the deck) | 0.26.x |
| A2 | Activity animations: run, lift weights, call, browse, pay, play an instrument, water plants, cook, wash dishes, fold laundry, drink at the bar | Performance engineer | 8 and 8b | 0.27.x |
| A3 | Player needs and activities, the walking-speed rule and the placeholder device | Player engineer (new) | new `// 15. PLAYER NEEDS & DEVICE`, plus small hooks in 11 | 0.28.x |
| A4 | Food and cooking: the galley rota, stock, cooking batches, servery and shelf, dish pit, meals eaten | Galley engineer (new) | new `// 16. GALLEY & FOOD` | 0.29.x |
| A5a | Utility rooms on Decks 4, 5 and 6, and the gym's treadmill (Deck 3, shared kit) | Deck 6 architect | `DECKS[4]`, `[5]`, `[6]`, kit | 0.30.x |
| A5b | Utility rooms on Decks 1 and 3 (recycler, galley plant, irrigation, relay room), plus gym weights and store till/basket kit | Bridge architect | `DECKS[1]`, `[3]` | 0.31.x |
| A5c | Utility rooms on Deck 2 (lab gas plant, utility closet, cable crawl, array plant as needed) | Command architect | `DECKS[2]` | 0.32.x |
| A6 | Roster touches: galley staff shifts, habits for the new activities | Crew designer | 9 | 0.16.x |

**Check-in with the user after Half A:** a ship that cooks, eats, works out, shops and calls home, and a player with needs and the activities that meet them.

### Half B: the ship needs looking after (starts on paper now, visible after Half A)

| # | Workstream | Owner | Section | Builds |
| --- | --- | --- | --- | --- |
| B1 | Machines and wear: a machine registry, condition, wear by use, the five states, consequences for needs and mood, ship health | Systems engineer (new) | new `// 17. MACHINES & JOBS` | 0.33.x |
| B2 | The job list: jobs from wear, crew claiming them, the Works job board, the player's job loop (inspect, carry two, repair) on the device | Systems engineer, with the player engineer for the player's side | 17, 15 | 0.33.x, 0.28.x |
| B3 | Supplies and carts: stock in the Deck 5 hold, parts, food restocking by hover cart and lift | Systems engineer, with the galley engineer for food | 17, 16 | 0.33.x, 0.29.x |

The systems engineer starts B1 now as data and logic with no drawing (machines in a list, wear and states over days, a `machine_check` in the style of `day_check`). It attaches machines to rooms as the A5 utility rooms land.

**End of Pillar 2:** the user's review.

The lead merges onto `claude/ship-integration` and numbers each combined build 0.40.0, 0.41.0 and so on.

## Shared formats

The owner of each may refine its details, but must tell the lead and keep the other sessions' side working.

### Activities on places (A1, A2, A5)

- **A place may carry `anim`**: what someone does there. The values are `run`, `row`, `lift`, `call`, `browse`, `pay`, `play`, `water`, `cook`, `wash`, `fold`, `drink`, `read` and `talk`.
- **Without `anim`,** the activity comes from the type:
  - `gym` → `lift`
  - `callhome` → `call`
  - `shop` → `browse`
  - `music` → `play`
  - `garden` (standing) → `water`
  - `laundry` → `fold`
  - `work:galley` → `cook`
  - The dish pit is `wash`.
- **The gym** already has three treadmills (3-gym-1 to 3-gym-3) and a rower (3-gym-4). They get `anim: 'run'` and `anim: 'row'`. The treadmill's belt scrolls and its console lights up while someone is on it (the Deck 6 architect's kit, driven by an occupancy hook).
- **The crowd and full rigs** take the activity as a pose: `handle.set(pos, face, pose, walkPhase)`, where `pose` may be any `anim` value as well as `walk`, `stand`, `sit`, `lie` and `work`. Unknown poses fall back to `stand`.
- **Props** (a phone receiver, a basket, a watering can, a pan): drawn by the crowd, kept cheap, and optional per pose.
- **New places** can carry an optional `y`. They're added by the architects, never by anyone else.

### Needs (A1, A3, B1)

```js
NEEDS = ['hunger', 'energy', 'hygiene', 'fitness', 'social'];   // 0–100, 100 = fully met
```

- **The player:** `SHIP.player.needs = { hunger, energy, hygiene, fitness, social }`. It's saved under the save's `player` (bump the save to `v: 2`, and still read `v: 1` saves by filling needs at 80).
- **Draining and restoring:** needs drain with ship time and are restored by actions. Eating restores hunger, sleep restores energy, showering restores hygiene, the gym restores fitness, and calling home or company restores social. The player engineer sets the rates and reports them.
- **Walking speed:** below a threshold of fitness, or of energy, you walk slower. That's the user's rule. Start at below 25 → 80% speed, each need counted separately. The player engineer tunes the numbers and reports them.
- **Crew** have the same needs on paper, but derived from their schedules (it's planning, not stepping): sleep, meals, showers, gym, calls home. Needs bias the choices in `planDay` (the sim engineer). B1 consequences push on needs and mood, for example a weak shower leaves hygiene lower.

### The device (A3, B2)

- **A placeholder panel,** opened by a small button. It holds your needs as bars, the time and day, and later your jobs.
- **Sections are registered:** `device.addSection(id, title, render)`. B2 adds a jobs section without touching A3's code.
- **The user will redesign the device.** Keep it plain and replaceable.

### Food (A4, B3)

```js
SHIP.galley = { cold: { meals: n }, servery: { portions: n, dish: 'name' }, grab: { items: n }, dirty: n }
```

- **Cold store stock** is in meal units.
- **Cooking:** a batch takes cook time at the ranges and ovens and moves stock from the cold store to the servery.
- **Eating:** eating takes a portion, and an empty servery means a queue and waiting.
- **Plates:** dirty plates go to the dish pit and are washed by galley staff.
- **On paper and on the deck:** the same sums run on paper when the player isn't on Deck 3 (like `whereIs`) and drive what you see when you are: food on the servery, the queue, the shelf filling.
- **The galley rota:** Chef Brennan rises early (about 04:30) and cooks breakfast before 06:00, and cooks again before 17:00. Galley hands' shifts follow the meals.
  - The galley engineer owns the rota rules (section 16).
  - The sim engineer consults them through a small hook in `planDay`.
  - The crew designer sets the galley staff's shift fields in the roster.
- **Saving:** the galley state is saved.

### Machines and jobs (B1, B2)

```js
// per deck, added by the architects as utility rooms and kit land:
machines: [ { id: '4-scrubber-1', kind: 'scrubber', at: [c, r], room: 's', face: 'n', panel: [c, r] } ]
// state, in SHIP.machines[id] = { cond: 0–100, state: 'healthy'|'worn'|'faulty'|'failing'|'broken', lastService }
JOBS: [{ id, machine, kind, urgency, posted, claimedBy, parts: ['filter'], status }]
```

- **Wear** runs on paper and is deterministic from the seed and use. For example, the oven wears at mealtimes, the washers after busy shifts, and the lift with every ride.
- **Effects** come in the staged consequences from the design doc.
- **Saving:** `SHIP.machines` and `JOBS` are saved.
- **Panel places** carry `machine: '<id>'`, so the schedules never hand them out as desks; they're used only for servicing and repairs.
- **One save hook for everyone:** `SAVE_EXTRA` (section 13, from the systems engineer) is a list of `f(save)` run before writing. Needs, the galley and machines all add their part through it.
- **Effects:** `shipEffects(deck)` (section 17) returns multipliers for need restore and drain, walking, cooking and the lift, plus mood and notes. The player engineer, the sim engineer and the galley engineer apply them.

## The utility rooms (A5)

- **What to build:** each architect builds the inside of its decks' sealed service rooms: machines, pipes, panels, a walkable floor where a person can stand to work, and the hatch as the way in. Every machine that will be in the registry needs:
  - a `machines` entry;
  - a `panel` tile where someone stands to service it;
  - a `work:works` place at that tile.
- **Access:** Works crew and the player can pass these hatches, but only into a room whose inside is built (the Deck 6 architect adds the shared hatch code and the deck_check rule first; each architect marks their rooms as built). Everyone else treats hatches as walls. Tier locks come later, with progression.
- **Crawlways** are standing floors with low trays for now; crouching comes later.
- **Plan first:** add a short "Utility rooms" section to that deck's plan page, with a sketch, and send it to the lead before building. The lead reviews it, and shows the user anything that changes a room's size or position.
- **New furniture for Half A:** the gym's treadmill (and weights if missing), the store's till and baskets, and anything else an activity needs. Each item gets a place with `anim`.

## Parallel-work rules (as before)

- **Stay in your own sections:** each session edits only its own sections and its own rows in DEV_NOTES. Shared code changes are minimal, inert for anything that doesn't use them, and reported.
- **Merge first:** start from, and regularly merge, `origin/claude/ship-integration`.
- **Report:** push to your own branch and report to the lead after each push.
- **The design doc:** `design-doc.md` is edited only on the lead branch. Send the lead the wording.
- **Tests every turn:**
  - `cadet_test.py` (with crew off where crew change on purpose);
  - `deck_check.py`, on all six decks;
  - `day_check.py` (one day; two days when schedules change).
  - Turns that add a checker extend `day_check.py` or add their own: `food_check`, `machine_check`.
- **Budget:** draw calls stay under about 450 on every deck in `day_check`. Props and new kit must keep that.

## Check-ins with the user

1. **After Half A:** a playable build where the chef cooks before each meal, crew use the gym, booths, store, garden, music room and laundry, and you have needs on a placeholder device and can work out, call home, shop, eat, wash and sleep.
2. **End of Pillar 2:** machines that wear, faults you can see, the job board, and you fixing things.
