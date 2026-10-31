# Handover: PL2 (seats, doors, Talk a while), 0.99.5 playtest patch

Role: builder for the user's playtest notes 3, 12 and 13 (2026-10-31), for lead 47. Reviewer RV29 (PASS 6b2f135; pl2.2 75e22d2 under re-review).
Branch: claude/p995-player, from claude/staging-0994 8976965e (0.99.4). Game commit 1c06638 (pl2.2), game sha256
f07b738a1541dcd66a6e78b49f3ac407814b07dad24db22a1ef5ef73806fccf0 (pl2.1 was 938f8b85 / e462d177...f80b). Build-number lines untouched (the build master's).

## What was built (all live, no feature switch)
- **13, locked rooms stay locked.** Cause: section 15 `jobDoorOpen`'s "a locked room you're standing in lets you out"
  (0.28.55) counted the hall on the other side of a locked door, so every 'closed' door off a corridor (Deck 4 officers'
  cabins, Deck 2 bedrooms, Deck 5 office/booth, Deck 6 reactor) let you in. Fix: `lockedBehind(room)` (Player engineer
  slot): rooms not reachable from the lift through door/open/lift edges and service hatches, YOU_LOCKS shut; cached on
  EDGES. (c), lead's GO: `adoorMineLocked(e)`; a locked door open to you follows the Doors setting (15b adoorKind,
  adoorPrivate, adoorShut, adoorSelfKey, adoorHint take 'closed'; 8c crewNearDoor asks adoorShut for you; section 11's
  tap on a closed door tries adoorTap first). Inside a private locked cabin under the default you leave by a tap.
  **Narrowed in pl2.2 (1c06638, RV29's FIXES NEEDED from BM23's round):** `lbGuards(room)`: only halls with a locked
  door into a bedroom (Deck 2 '-' '+', Deck 4 '-') stop opening; every other locked room (Works Chief's office, booth,
  ready room, reactor) is as 0.99.4, since meetings (intro d2-solo), summons and visits walk in through that rule.
  Backlog (keys as BM23 merged them): PL2-1 = Talk a while +15 social, PL2-2 = the other locked rooms still open from outside.
- **12, Talk a while ends on its goodbye.** `talkPlanEnd(C)` (my slot) predicts the wrap-up slot; section 20 talkStep
  keeps `T.endAt`, `T.u` (progress in 15-minute units) for social, friendship and the full end; talkMeter shows the real
  minutes left. Not a pack talk: exactly as before. A stopped talk now earns its share of the real length.
- **3, Take a seat everywhere.** section 15 seatBtnSeat/seatBtnGo: no tray, the nearest free SIT_TYPES seat in your room
  on any deck, a plain sit; tray path unchanged; rec seats out. `SEAT_BTN_ALL` (off at test URLs unless ?seatbtn).

## Check edits (owners to review)
talk_check.py (small talk's step test ignores the final end step), social_check.py (Stop expects floor(T.u/5) points).

## How to test
player_check (alone, own CADET_WORK), interactions_check (~64 min, background timeout > 1 h), talk_check, social_check,
deck_check, day_check 3 and 6, check_fast, cadet_test vs 8976965e (ALL IDENTICAL). Probes in a scratch folder used
`Game` from cadet_test.py; nearestOpen takes world x, z (not a cell). The "go to your new cabin" arrow opens doors on
its way by design (adoorWay), so stub it when probing your own cabin.

## Loose ends / open questions
- Not probed: an invited friend's cabin in the real game; controller X on the seat button.
- A full talk shows +15 social in probes on both builds (30 expected by the design); backlog PL2-1, not chased.
- intro_check whole takes ~40 min on this host (guide says 11); give background runs a timeout over 50 min.
