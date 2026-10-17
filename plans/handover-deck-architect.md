# Handover: the deck architect (all six decks)

Written at build 0.38.9 (`claude/decks-p3` 3b28718) by session_014PT5L2QxXYoVhqFP7qhj3y, at about 55% of memory, ahead of Pillar 4's wave 2. Read it with CLAUDE.md, DEV_NOTES.md (the 0.38.x rows and the section "Places for Pillar 3"), plans/pillar4-plan.md (Part 6, seat 8) and the three older architect notes: `plans/handover-bridge-architect.md`, `-command-architect.md` and `-deck6-architect.md`. Read their newest versions on `claude/deck1-scale`, `claude/deck2-command` and `claude/deck-architect`.

## Role, branch, builds

- **Role:** the one architect for every deck's data: `DECKS[n]` (places, machines, rooms, dress), deck kit, gathering venues, event dressing and visit rooms. It replaced the bridge (Decks 1, 3), command (Deck 2) and Deck 6 (Decks 4-6) architects.
- **Branch:** `claude/decks-p3`. **Builds:** 0.38.x; the last is 0.38.9. Bump both the header line (`build 0.38.x`) and `GAME_BUILD`, and add a DEV_NOTES row each turn.
- **Lead:** session_01PxXKwc5mkC7tV5MPi3p7PP (as of 2026-10-17). Report after every push with send_message: commit, what, checks, judgement calls.
- **Merging:** before a job, merge the latest `claude/ship-integration` (or the branch the lead names). The conflicts are always the two build lines (keep yours) and DEV_NOTES rows (keep both; watch for duplicate rows the lead already copied).

## What I built (0.38.0-0.38.9)

All in one block just after `DECKS[1]` (search `Big gatherings (Pillar 3`), plus a few lines inside the decks:

| Build | What | Where / names |
| --- | --- | --- |
| 0.38.0 | Gathering venues | `DECKS[3/5/1].gathers`; spots become places `<deck>-<venue>-crowd-<n>` / `-lead-<n>` (type `event`, `gather`); `gatherSpots(venue)`, `gatherVenue(venue)`. Venues: plaza, mess, bow-lounge, shuttle-bay, works-bay, observation |
| 0.38.1 | Event dressing and traces | `DECK_DRESS`, `dressShow(list)`, `dressingOn()`: signupMess, signupWorks, stormRosterTeaCorner, relayScorch, tapedPanel, partyLounge. Section 18 calls `dressShow` once a ship minute (wired by the events engineer) |
| 0.38.2 | Visit rooms, gym kit | `DECKS[n].visits` + `visitSpots(id)`: ready-room, captain-table; gym 3-gym-11..14 (rowing pair, `punchBag`, `gymMat`) |
| 0.38.3 | Conference visit | `visits.conference` (observation room table) |
| 0.38.4 | Patient beds | `3-ward-1..4`, type `patient-bed` (deck_check accepts it) |
| 0.38.5 | Diplomatic visit | `veyliCordSculpture` in DECK_DRESS; shuttle-bay leads are now Captain, Saruth, Speaker |
| 0.38.6 | Working garden | `3-gardenwork-1..5` (`work:garden`), machines `3-growlight-1/2` with `-panel` places, `3-crates-1` (storage) |
| 0.38.7 | Garden beds | `raisedBed` crop `roots`; three root beds (`live: 'roots'`) and a third bean trellis (`live: 'beans'`); crates moved to [9,12] |
| 0.38.8 | Washers | `4-washer-1..4` real machines with `4-washer-N-svc` places |
| 0.38.9 | Arrival evening | `keepsakeShelf` above berth 4's bunk + `DECKS[4].keepsakes` (slots, place `4-B1-4-keepsake`); `mugRack` in the Works tea corner + `DECKS[5].mugRack.yours`; `CALM_TYPES` / `placeCalm(p)` |

## Loose ends

- **machine_check FAIL since 0.38.8:** "two jobs at once: kovac-zainab", which appears only once the washers are real. It's section 17's job-claim overlap. I reported it to the systems engineer (session_01TqLepvhqDZRwFj7ZuLb6Xa); check it was fixed.
- **Spare stations reshuffle:** `work:garden` (0.38.6) joined section 14's spare list, whose stand-in draws use list position (`schedU(9001 + i)`). Any new `work:` place type nobody holds shifts other stand-ins. I suggested keying by place id to the sim engineer (session_01R6RBwwBM9aorpsqDCrztDU).
- **Calm tags** are type-based (`CALM_TYPES`). If the social engineer wants exceptions, add `calm: false` (or `true`) on those place lines.
- **Keepsake slots** are data only; the performance engineer draws the instanced keepsakes there.

## Part 6, seat 8: still to do (wave 2 and later)

From plans/pillar4-plan.md seat 8, not started:
- seedling pots in the garden (yours marked once planted);
- the Tiles station in the bow lounge, plus a board on every lounge table for Tiles night (one instanced mesh, at most 3 draw calls);
- the postbox by the call-home booths;
- the tasting board in the mess;
- lantern places along the promenade;
- decor for each new tradition, within its budget: at most 6 draw calls, only on its deck, only during its window. Use the DECK_DRESS pattern, or section 18's `EV_KIT`, as the traditions engineer prefers.

## Gotchas (learned the hard way)

- **New places aren't automatically inert.** Type `event` with no `event` field lands in schedData's unused `n|event` pool: inert. A new `work:<x>` type joins the spare list (see above). A place in a room with a bed becomes that bed's private place, unless its id starts with a bed id (then only that bed owns it). Always compare crew plans before and after: in a scratch script, hash `[1,2,3,5,8].map(d => schedPeople().map(p => [p.id, planDay(p, d)]))`.
- **R():** kit that draws `R()` (raisedBed, trellis, shelving) goes last in a deck's `dress()`. Shared kit made at load never calls it.
- **Machines:** `face` is the way the front faces, toward the panel. There must be exactly one `work:works` place with `machine: id` on the panel tile; Deck 4 names it `-svc`, Decks 1-3 `-panel`. A kind missing from `MACHINE_KINDS` is dropped silently.
- **Wall pieces hide when their wall is lowered.** Shoot them with walls on auto, from a camera angle that faces the wall.
- **Tall things** (bunks, racks) fade, so a shelf on the wall behind them can still be seen.
- **cadet_test only covers Deck 4.** Anything you add to Deck 4 shows in `a_start`/`b_wander10s`. Crop the differing box and check it's only your piece.

## How to test

Setup: `pip install playwright`; three.js r128 in `/tmp/cadet-work/three` (`npm pack three@0.128.0`); `CADET_CHROME=/opt/pw-browsers/chromium`. Run from a scratch folder, one at a time:
`cadet_test.py OLD NEW`, `deck_check.py NEW`, `day_check.py NEW 1`, plus `events_check.py` (gatherings, dressing), `machine_check.py` (machines) and `tools/kitdup.py` from `claude/lead-pillar1` (duplicate KIT names).

## Open questions for the user

- Should the gathering venues get a visible marker when a gathering is on (a rope line in the shuttle bay, chairs set out in the observation room)?
- The Captain's table: she sits at the north end and you at the south. Is that right?
