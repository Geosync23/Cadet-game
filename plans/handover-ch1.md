# Handover: CH1 (characters and seats, 0.99.7 playtest patch)

Role: builder for lead 49, notes 1, 4, 10, 35, 37 of plans/patch-0997.md (on claude/lead-49). Reviewer: RV32.
Branch: claude/p997-chars, from claude/integration d7ad4c58 (0.99.6). Commits: 3d07e66 (batch A), 8436ff6 (batch B), then this note.
Game sha256 at 8436ff6: c574f6c2...41414434. Build-number lines untouched.

## What I built (all switched off; off = 0.99.6, cadet_test ALL IDENTICAL)
Section 8 has a new slot, "CH1 characters", at its end (comment lines plus my code). Switches there:
- `CH_SOLE_ON` (37): makeCharacter skips the flat sole box under each boot.
- `CH_POSE_ON` (35): 8c `slump`, the hands-on-belly variant becomes hands resting at the sides (armTo .12, -.55, .17, .2). Auditorium seats and the rec beanbags.
- `CH_RELAY_ON` (10): Deck 4 room 'y' breaker cabinet (machine 4-junction-2, "Light relays") at lz `CH_RELAY_Z` 3.3 instead of 3.65 (it went through the curved hull); the machine's look.lamp/drip z moved by the same at load.
- `CH_HAIR_ON` (1): hair caps + `CH_HAIR_PAD` 0.008; 8b crowdGeo makes coarse caps with `chCapOut` (radius over the cos of half a segment each way) so skin can't show through.
- `CH_SEAT_ON` (4): `CH_SEATS` table (placeSpot hook in section 10 -> `chSeatSpot`), `CH_FEET` + `chFeet` (feet on the step in the stands and auditorium; hooks in 8b's sit legIK and 8c's slump legIK), sofa kit's throw cushion not drawn (4b).

Hook lines outside my slot (owners to review): 4b sofa (one `if`), 4d Deck 4 place('y', 'breakerCabinet'...), 8 makeCharacter sole and cap lines, 8b crowdGeo and the sit legIK, 8c slump (arms and legIK), 10 placeSpot.

## How to test
- A switched-on copy: `sed -e 's/^const CH_SOLE_ON = false;/const CH_SOLE_ON = true; /'` (same for CH_POSE_ON, CH_RELAY_ON, CH_HAIR_ON, CH_SEAT_ON).
- cadet_test base vs off (ALL IDENTICAL), check_fast, deck_check on the on copy (OK at 8436ff6).
- plans/ch1-seat-probe.js: paste into a game page (cadet_test's window.__sc) on a loaded deck; lists sit places with something inside the seated body and the nudge that clears it. Faded groups (promenade planters) are not seen by it.
- `?seats` (8b's seat demo) puts a stand-in on every seat of a deck: the quickest way to look.

## Loose ends / questions for the user
- Defaults taken (overnight): only the hands-on-belly auditorium variant changed (hands behind the head stays); the beanbags change too; soles go everywhere, the rec grip socks' coral soles too; sofas lose their throw cushion.
- Not changed: seats whose back is 12-15 cm behind the spot (mess, bow lounge sofas, 2-armchair-9..12, 6-watch) touch the back of the torso by a few cm; add rows to CH_SEATS (about 0.05 forward) if the user still sees it.
- The seated legs are short for chair height, so thighs slope into the front of deep seats; the old cushion rule (place `cush`) covers sofas and booths. A general fix would be a pose change for everyone, not done.
- Event-only furniture (7-ring chairs, the long tables, the piano) wasn't on deck when probed; not checked.
