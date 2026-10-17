# Handover: the deck architect (all six decks)

Written at build 0.38.9 (`claude/decks-p3` 3b28718) by session_014PT5L2QxXYoVhqFP7qhj3y, at about 55% of memory, ahead of Pillar 4's wave 2. Read it with CLAUDE.md, DEV_NOTES.md (the 0.38.x rows and the section "Places for Pillar 3"), plans/pillar4-plan.md (Part 6, seat 8) and the three older architect notes: `plans/handover-bridge-architect.md`, `-command-architect.md` and `-deck6-architect.md`. Read their newest versions on `claude/deck1-scale`, `claude/deck2-command` and `claude/deck-architect`.

## Role, branch, builds

- **Role:** the one architect for every deck's data: `DECKS[n]` (places, machines, rooms, dress), deck kit, gathering venues, event dressing and visit rooms. It replaced the bridge (Decks 1, 3), command (Deck 2) and Deck 6 (Decks 4-6) architects.
- **Branch:** `claude/decks-p3`. **Builds:** 0.38.x; the last is 0.38.9. Bump both the header line (`build 0.38.x`) and `GAME_BUILD`, and add a DEV_NOTES row each turn.
- **Lead:** session_01KPJMYjXAPkNUcrQ8VRkhLE (from 2026-10-17 ~04:35; the user's rule: refresh this note right before handing over; before that session_01PJtmxWgAPLebXSZKP6ZRpG and session_01PxXKwc5mkC7tV5MPi3p7PP). Chain of command: the user → the lead → everyone; helpers never contact the user.
- **Holder since 0.38.10:** session_01ToE6RJFCw9deB3HcJRLKxS. Report after every push with send_message: commit, what, checks, judgement calls.
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
| 0.38.10 | Sowing morning, Tiles | kit `seedlingStand` (garden NE corner), `DECKS[3].seedlings`, place `3-seedlings-1` (`sowing`), trace `seedlingYours`; kit `tilesTable` (bow lounge), places `3-tiles-1/2` (`tiles`), `TILES_KIT`/`tilesBoardGeo()`, `DECKS[3].tiles`, `tilesSeats(k)`, dress `tilesNight` (one InstancedMesh) |
| 0.38.11 | Letters, tasting, lanterns, calm | kit `postbox` + `3-postbox-1` (`letters`); dress `tastingTable` (title, lines), `lanternWalk`; `3-lantern-1..12` (`lanterns`); calm false on 3-wbench-1/2, true on 2-obsnight-1/6/7 and the Tiles stools |
| 0.38.12 | Review fixes | `TILES` renamed `TILES_KIT` (section 23 owns `TILES`); every Tiles-night board names at least two seats (sixth field) |
| 0.38.17 | Tiles, approved design | `TILES_KIT` repainted; taps 'Tiles station' / 'Tiles board' (one per Tiles-night board via dressShow's `more`); trace `tilesTrophy` (Deck 4, `DECKS[4].keepsakes.trophy`) |
| 0.38.18 | The walk-in Tern (plans/shuttle-plan.md) | kit `shuttle` rebuilt (aisle, benches, cockpit, lockers, roof group hidden inside, hinged ramp); `DECKS[5].tern`; places `5-tern-*`; `ternRamp`, `ternRampOpen`, `ternInside`, `ternClear`; shuttle-bay venue focus/leads moved. On ship integration 0.60.2. |
| 0.38.19 | Tern review fixes | the ramp never closes on anyone (`ternRamp` returns false; a close in progress waits); the well blocks below half-open; plan numbers; rota-day note |
| 0.38.20 | Long-table seats | `3-longtable-1..13` (`event: 'long-table'`): mess end chairs and a promenade trestle, drawn by `longTables` / `harvestTables` via `messExtra` / `MESS_EXTRA` |
| 0.38.14-16 | Traditions' asks | places `2-open-lab-*`, `1-bridge-hour-*`, `4-music-1` (`late-piano`), lantern places `lantern-walk`; traces `mugYours`; dress `longTables`, `harvestTables`, `cupBoard`, `talentStage`, `yearsEnd` (Deck 3), `openLab` (Deck 2). Mending day, rummage day and the crossover supper were cut by the user. |
| 0.38.9 | Arrival evening | `keepsakeShelf` above berth 4's bunk + `DECKS[4].keepsakes` (slots, place `4-B1-4-keepsake`); `mugRack` in the Works tea corner + `DECKS[5].mugRack.yours`; `CALM_TYPES` / `placeCalm(p)` |

## Loose ends

- **machine_check FAIL since 0.38.8:** "two jobs at once: kovac-zainab", which appears only once the washers are real. It's section 17's job-claim overlap. I reported it to the systems engineer (session_01TqLepvhqDZRwFj7ZuLb6Xa); check it was fixed.
- **Spare stations reshuffle:** `work:garden` (0.38.6) joined section 14's spare list, whose stand-in draws use list position (`schedU(9001 + i)`). Any new `work:` place type nobody holds shifts other stand-ins. I suggested keying by place id to the sim engineer (session_01R6RBwwBM9aorpsqDCrztDU).
- **Calm tags** are type-based (`CALM_TYPES`). If the social engineer wants exceptions, add `calm: false` (or `true`) on those place lines.
- **Keepsake slots** are data only; the performance engineer draws the instanced keepsakes there.

## Part 6, seat 8: status

All of seat 8's places are built (0.38.9-0.38.12). Still to do: decor for each new tradition when the tradition designers ask (DECK_DRESS, at most 6 draw calls, its own deck only). The traditions engineer (now Traditions engineer 2, see TEAM.md; the first, session_018WZccmSvEfz2LC7DCfxdii, has handed over) lists a tradition's `ties: decor <id>` to dressShow from 30 minutes before to 15 after, and Sowing morning's `trace: seedlingYours` pushes `{ id, day }` to SHIP.traces. The Tiles engineer (session_01DG3in6CvFFta6NrLpoVCJV, section 23) may change the board's look once the user approves the design; keep the station and boards simple until then. When the Tiles game is built, its station places can become `lounge-seat` (this changes crew plans, to be explained then).

**In flight (as of 0.38.20, a71ac47):** the onboarding engineer (session_01KaHzfqSqF8B4bkNFrH1tsx) wires the arrival scene to the Tern (ternRamp(true, 2.5) after the fade-in, ternRamp(false, 3) once ternClear()); SHIP_START_ARRIVAL (sim engineer 4, session_01EJUGywZv9BpcUezjXES9AC) and INTRO_START (section 21) move from [7, 8] to 5-tern-aisle-1 [5, 7], face 0, in the same combine as the hull. Traditions engineer 2 and sim engineer 4 point the Sunday table and harvest supper at '@long-table'. Reviewer 2 has 0.38.17-0.38.20 to review. Waiting on Tiles (section 23 pushes the tilesTrophy trace).

## Gotchas (learned the hard way)

- **New places aren't automatically inert.** Type `event` with no `event` field lands in schedData's unused `n|event` pool: inert. A new `work:<x>` type joins the spare list (see above). A place in a room with a bed becomes that bed's private place, unless its id starts with a bed id (then only that bed owns it). Always compare crew plans before and after: in a scratch script, hash `[1,2,3,5,8].map(d => schedPeople().map(p => [p.id, planDay(p, d)]))`.
- **R():** kit that draws `R()` (raisedBed, trellis, shelving) goes last in a deck's `dress()`. Shared kit made at load never calls it.
- **Machines:** `face` is the way the front faces, toward the panel. There must be exactly one `work:works` place with `machine: id` on the panel tile; Deck 4 names it `-svc`, Decks 1-3 `-panel`. A kind missing from `MACHINE_KINDS` is dropped silently.
- **Wall pieces hide when their wall is lowered.** Shoot them with walls on auto, from a camera angle that faces the wall.
- **Tall things** (bunks, racks) fade, so a shelf on the wall behind them can still be seen.
- **Floating need notes** ("+69 Energy") fade on real-time timers and can make one cadet_test shot differ; re-run (the combined build's cadet_test hides them).
- **`DECK_DRESS` disposes** every geometry and (since 0.38.13) every material except the cached `DRESS_MATS` colours and `HIT_MAT` when hidden. So a dressing must never borrow a shared kit material (`M.*`, `LNG.*`, `GD.*`, `TILES_KIT.mat`): use `dressMat(colour)` or its own. Give instanced meshes their own geometry, material and texture clone, and set `noMerge` and `frustumCulled = false` on them.
- **cadet_test only covers Deck 4.** Anything you add to Deck 4 shows in `a_start`/`b_wander10s`. Crop the differing box and check it's only your piece.

## How to test

Setup: `pip install playwright`; three.js r128 in `/tmp/cadet-work/three` (`npm pack three@0.128.0`); `CADET_CHROME=/opt/pw-browsers/chromium`. Run from a scratch folder, one at a time:
`cadet_test.py OLD NEW`, `deck_check.py NEW`, `day_check.py NEW 1`, plus `events_check.py` (gatherings, dressing), `machine_check.py` (machines) and `tools/kitdup.py` from `claude/lead-pillar1` (duplicate KIT names).

## Open questions for the user

- Should the gathering venues get a visible marker when a gathering is on (a rope line in the shuttle bay, chairs set out in the observation room)?
- The Captain's table: she sits at the north end and you at the south. Is that right?

## Deck architect 3 (2026-10-17 evening, claude/poses, builds 0.27.42 and 0.27.44)

Session_01NsysH87qqJnf1dBEVRz2fW, reporting to lead 8 (session_01FutyR6xiAmZv29oS4TWKdS); reviewer 1e (session_01BcEWju7cay3mnujaL1apzU). Two small jobs on perf 3's build line; DEV_NOTES rows 0.27.42 and 0.27.44 have the detail.
- **0.27.42, toilets on Deck 4 (passed by 1e):** a WC sign on the shared `toiletStall` door (`KM.wcSign`), so every toilet stall on Decks 2, 3, 4 and 5 has one. `washroom()` takes `o.wc` (default 1); Deck 4's p and q use 2: one shower, two toilets each. Open for the user: 6 juniors a day now wash at a basin instead of a shower; to undo, drop `{ wc: 2 }` and swap the places 4-toilet-p2/q2 back to showers.
- **0.27.44, shallower deep seats:** the `armchair`, `sofa` and `beanbag` kits end their seat about .12 ahead of centre (footprints unchanged). Their 36 sit places carry `cush: .2` (seatCushion casts at .2 × height there, found by position in `SEAT_RC.cushK`) and sit .23 behind the front edge. **Any new sit place on an armchair, sofa or beanbag needs `cush: .2` and a spot at local z -.105 (armchair), -.11 (sofa) or 0 (beanbag), facing the way the piece faces.** Without the tag, the ray misses the shallow seat, the feet go to the floor, and the thighs dip through the front.
- **Possible later tidy-up (lead's option B, not now):** ray .2 × h for every seat. It would also lift the thighs of short sitters on chairs whose seat reaches .18–.33 m ahead (bridge chairs, lounge bar/booth seats, some mess chairs, call booths); it changes pixels on most decks.
- **Probe scripts (scratchpad, not committed):** seatprobe.py (shortest, tallest and broad stand-ins on every seat place: front edge, knee, shin samples inside the seat), deepmap.py (sit places on a kit, in the kit's own frame; wraps `KIT[k]` before a deck load), seatshot.py (stand-ins on chosen seats at phone zoom). Gotcha: cadet_test.py's top half defines `HOOK` and `instrument()`. Don't reuse the name `HOOK` in a script that execs it, or the page never gets `__sc`. Two test runs on the same build at once share `/tmp/cadet-work/test/_run_<name>.html` and time out; copy the file under another name first.
