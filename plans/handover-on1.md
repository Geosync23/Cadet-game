# Handover: ON1, the onboarding builder for playtest patch 1 (section A)

Written 2026-10-22 ~06:35 UTC by ON1 (session_01BJNi1oqxnQ3jUusXHbHDGW). Lead: lead 26 (session_015mHBLCf5jpnzBkFY1iBTqv). Reviewer: OR2 (session_01AnRKXUUGi8mwREwvt4WbaV), **PASS at 8c8bf8fd**.

## Branch and builds
- `claude/patch-play1-a`, from claude/integration 32b699a6. Reviewed tip **8c8bf8fd**; this note is a docs-only commit on top. The build number is BM13's (untouched).
- The build-table row is "patch-a (ON1)" in plans/build-table.md; DEV_NOTES "The arrival (section 21)" has a "Playtest patch 1" bullet; design-doc.md "Arriving by shuttle" and "Clothes and laundry" are updated.

## What I built (notes 1-6 and 8; note 7 went to CJ1)
1. The arrival is at 16:30 (`INTRO_START`, 13's `SHIP_START_ARRIVAL`). The Day 0 steps are an hour earlier and `INTRO_ESCORT_UNTIL` is 18:00. The evening's latest times moved only half an hour, for a slow player: the Chief's fallback and 'free'/'tomas' at 19:00, 'night' at 19:30.
2-4. New steps 'stow' and 'device' after 'bunk', with the step fields `reach` and `ready(t)` read by introAdvance.
   - You put your bag in your wardrobe yourself: 21b's `wardrobeUse` stows it first, and 15's `bagLockerTap` acts only at the wardrobe. The arrow is `INTRO_ARROWS.stow`.
   - His wardrobe lines follow as the 21b beat 'd0-wardrobe' (a seek beat while you're in Bunk 1).
   - Then the meeting `introDevice` (content/meetings/introDevice.meet), with `introDeviceGive` as it opens.
   - The cabin Mail is parked: `ZEKE_CABIN_MAIL = false`.
5. The Chief's walk to your table lasts until her welcome is over (`INTRO_CALDER_UNTIL` 20:00 is only a cap). `introCalderIn` reads her seat from the chief step itself.
6. `INTRO_LINGER` is 10 ship minutes: Zeke through `introLingers` in escortPlan, Calder through a second crewComeTo.
8. `CLOTHES_FRESH` gives +8 hygiene on a change; `clothesDirtyTick` shows the dirty-clothes drain as "−2 Hygiene".
- Also: walk.goodnight.1 says breakfast from seven (SC1), and the Day 1 tea arrow points at the tea table (FR4's note 10).

## Checks (on 8c8bf8fd)
- intro_check: full OK, --evening OK, --dawdle OK (it FAILS on 32b699a6, which proves the note 5/6 checks), --week OK.
- clothes_check: ALL OK. player_check: OK. device_check: OK. lines_check: PASS.
- career_check: only the known backlog-12 failure.
- check_fast: OK. cadet_test against 32b699a6: ALL IDENTICAL.
- intro_check part 8 now runs with `CLOTHES_ON = true` and taps the wardrobe (WALK_TICK).

## Loose ends
- **SC1 (breakfast 07:00, claude/patch-play1-f) moves the crew's wake time.** Tomas's Day 1 'd1-wash' beat (06:00-06:30, Bunk 1) may find him asleep. I asked SC1 for its tip and got no answer before handover. After the merge, run `intro_check --week` and look at d1-wash; if needed, move its `at` to his new wake time.
- **Note 7 (the Chief's Day 2 solo job) is CJ1's.** CJ1 edits introWeekMeetings, introMeetEnded and introSoloJob.meet; we agreed lines with no overlap.
- **Small edits in section 15 for the player engineer to review:** bagStow's text, bagTick, bagLockerTap. player_check's kit-bag test changed to tap the wardrobe.

## Gotchas
- At a test URL (?nosave) clothes are off, so the wardrobe tap does nothing: set `CLOTHES_ON = true` before newGameStart(true) in a check.
- While you stand on his wait tile [8,3], Zeke waits in the doorway [8,4], which is the Junior corridor. Room-based tests that need him in Bunk 1 fail there.
- `introSeat()` returns null once the step is past 'free'; a late Chief welcome comes after 'free'.

## The Zeke fix (0.64.16; lead 27; branch claude/patch-zeke from claude/integration 2b4a05db)

**The user's report on 0.64.15:** after Zeke shows you where to put your bag, he stops and stands in the bunk room.

**Cause:** introAdvance's hold, "his own steps never time out while he's within 10 tiles of you, until 18:00", also covered patch A's 'stow' and 'device' steps. Those wanted you inside Bunk 1. If you stepped out into the corridor, or missed the bag tap (patch A had narrowed it to the wardrobe), he waited until 18:00. The 'bunk' and 'table' talk steps had the same hold (OR2's find).

**Fix (section 21; `bagLockerTap` in 15):**
- `noHold` on 'stow' and 'device'.
- `near: 3` on 'device': escortPlan 'follow' on its deck brings him to you; any room counts for its meeting.
- A wait/meet step holds near you at most `INTRO_HOLD_MAX` 8 minutes, and only while he is near you. A slow player away from him keeps the full wait (intro_check part 2 caught that version).
- A 'bunk' missed with you near him goes on to 'stow' (`laterNear`); missed while away, it skips them as before.
- A reload that lost the device scene still hands the device over.
- A New game closes an open arrival scene (`introUiReset`).
- A tap anywhere in Bunk 1 with the bag walks you to your wardrobe again.
- If you never come near him, the device waits for Monday's briefing, as before (part 2 checks that).

**Checks:**
- intro_check parts 14 and 15 (`--leave`): stay without stowing; the corridor after or without the bag; the lift to Deck 3; a reload in the device step; near him but not at the spot during 'bunk' and 'table'. All FAIL on 2b4a05db and pass on the fix.
- The full intro_check: see the last message to lead 27 and OR2. Part 10 now signs in through the form (a click timed out once under load).
- check_fast: OK.

**Build number:** BM13 put 0.64.16 on top of 40fbd0d5 (88ea31f2); the later commits need it re-based.

**Gotchas from this round:**
- Don't run check_fast alongside the full intro_check: the load made a Playwright click time out.
- Never `pkill -f` with a pattern that also appears in your own command line; it kills your shell (exit 144). Build the pattern from pieces.
