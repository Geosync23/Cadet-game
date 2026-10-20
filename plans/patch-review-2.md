# Patch reviews: PR2

The playtest patch reviewer from 2026-10-20 ~19:15 UTC, taking over from PP1 (`plans/handover-patch-planner.md` on claude/patch-plan). Reports to lead 21. Owner and hook reviews are OR1's (claude/owner-review-1) since 19:36.

How each review is done (PP1's method):
1. `tools/section.py --diff`.
2. The build-number lines are untouched.
3. check_fast in a worktree.
4. cadet_test BASE→HEAD, alone on the machine.
5. intro_check where the arrival changes.
6. A probe of my own at 390×844, looking at the shots.

Probes live in `plans/patch-review-2/`.

Harness gotcha (new): speech bubbles pop in with a real-time CSS animation (`.bub` → `bubIn`), which never runs under the test's virtual clock. Their card stays at opacity 0 in screenshots although `display` is block. Add `.bub{animation:none!important}` before taking shots.

## PA batch B: claude/patch-a 8ee5d6b (#15, #3, #4, #14). PASS WITH FIXES

- **Checks:** check_fast OK (325 s). cadet_test 4de6dbb→8ee5d6b ALL IDENTICAL (noise only). intro_check parts 1-9 and 11 clean; part 8: "the Chief 0 m from hers at the next table". My run hit its 25-minute limit in part 10.
- **Probe `rvB.py`** (the arrival evening in the real game):
  - #3: the Chief sits at 3-mess-26 [29,4] through the dinner chat, walks on "Look who's coming over", and is seated at 3-mess-9 before introChief.
  - #4: the four goodnight bubbles 18:56-19:02. `introHush()` is true throughout and false 4 s after. No other bubble until 19:06. The bubble is readable at the table (`rvB_goodnight_1.png`).
- **Fix 1 (#14):** from the handover in Bunk 1 (18:16) until the first open, the "Tap your device" pointer covers the needs strip's first three bars, and it shows over the introBunk dialogue (`rvB_pointer_dialogue.png`). Hide it during dialogues and cap it at about 30 real seconds, keeping the glow.
- **Nits:**
  - The `LINES['tip.device.first']` lookup is dead.
  - Positions are written every frame.
- **Note to the lead:** how a day runs is now only said if you're within 6 tiles at the goodnight.

## PE #26 First Light Cocoa: claude/patch-e cf45e2a. PASS WITH FIXES

- **Checks:** check_fast OK (300 s). cadet_test a0bd82a→cf45e2a ALL IDENTICAL (switch off).
- **PE's `e26.py` with `&firstlight&mug`:**
  - Day 1 only, 20:00-20:45.
  - Join: a free cocoa, sit:cocoa, three tips of five (holt, brennan, sato), Tomas, three replies, rel given.
  - The dim: hemi 0.85→0.55.
- **Fix 1 (bug):** `flcTick` calls `bubbleSay(z, line)` with the DECK_CREW record, not its handle `z.h`. bubbles.update reads `w.h` as a height, gets NaN, and the bubble stays `display:none`. Proven in-page: `bubbleSay(z.h, …)` at the same moment shows.
- **Fix 2 (bug):** `FLC_SHOWN` isn't saved, but `SHIP.events.joined` is. A reload in the lounge before 20:45 replays the meeting, and its rel can be earned twice.
- **Fix 3 (plan):** the Day 1 bed arrow shows 19:00-20:00, before the cocoa. Hold it from the invite until the tradition ends.

## PA batch C: claude/patch-a eb638e7 (#11, #12, #13, #17, #18, #19)

- **Checks:** check_fast OK (297 s). cadet_test 8ee5d6b→eb638e7 ALL IDENTICAL.
- intro_check and the probe: see below once run.
