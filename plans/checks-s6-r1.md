# 0.95.0 full round: runner R1 (AS1)

- Build: `claude/staging-p5s6` e0084ca9, game sha256 `d1666007e449f9bdcfc01d3f2f2c2a60dfeb866b46ddb23404c38df56f59f278` (matched).
- OLD: 0.94.0, integration 6f1915cb, game sha256 `5f4c5415...0a0f` (matched; not needed: no FAIL that OLD could explain, Step 6 isn't in it).
- Checks from e0084ca9, run 2026-10-27 from 18:00 UTC, two browsers, each its own CADET_WORK.

| Check | Result | Key lines |
|---|---|---|
| player_check (with the night part) | OK | PLAYER CHECK OK (764 s) |
| devmode_check | OK | DEVMODE CHECK OK |
| bubble_check | OK | BUBBLE CHECK OK |
| puzzle_check (p6, p7, p8, point) | OK | PUZZLE CHECK OK |
| social_check | OK | SOCIAL CHECK OK |
| talk_check | OK | TALK CHECK OK |
| day_check 4 | OK | DAY CHECK OK |
| day_check 11 | OK | DAY CHECK OK |
| arrows_pointer_check | OK | arrows_pointer_check: OK |
| dev_arrow_check | OK | DEV ARROW CHECK OK |
| arrows_check (default parts) | OK | ARROWS CHECK OK |
| arrows_check step5 | handed to R3 (free slot), see R3's notes | |
| arrows_check step6 asis / teachoff / track / skiptea | **FAIL (NEW)** x4 | stuck from Day 23 22:20 at m23:badge "Take a badge" (Deck 6); "the welcome: its level-1 arrow (pu4:welcome) never led" |

## The step6 FAIL: one game gap, one check gap

- **Game gap, NEW (28c, S6-5 night 2; not on the known-old list; OLD has no Step 6):** night 2's level-1 arrows point at
  rooms, not the things to tap. `M23_GOAL.badge` and `.return` are `{ deck: 6, room: 'K' }` (the dosimeter rack is place
  `6-dosi-rack`, a tap on "Dosimeter rack"); `.reactor` is `{ deck: 6, room: 'R' }` (the side job's stops are at
  `panelPlace('6-reactor-1')`). Every other step arrow (m23:n1, the tea table, the job board) points at the thing.
  Proof on a copy of e0084ca9 with badge and return given `place: '6-dosi-rack'` and the reactor's goal
  `place: panelPlace('6-reactor-1')`: step6 asis OK, all 13 beats (night 2's permit, badge, tell, reactor, out, badge
  back all led), missed 0, stuck 0. Without it (e0084ca9 with the fixed check): FAIL "the reactor (night 2): not
  reached", stuck from Day 23 21:56 at "Take a badge".
- **Check gap (fixed, claude/arrows-step6 10ab714a, test only):** 28c's coil-balance card shows both coils ("Coil 1
  running hot. Coil 2 a little cool."); the follower read "cool" and pressed + on Coil 1 from 00:29 to about 05:50, so
  night 1 ran over and pu4:welcome never led. It now reads its own coil (the card's heading). Also: m23 in S6_RX and two
  beats, 'engine work (night 1)' (side.m23.d1) and 'the reactor (night 2)' (side.m23.d2).

**R1: NO-GO on e0084ca9** until 28c's night 2 arrows are fixed; then step6 x4 again with the fixed check.
