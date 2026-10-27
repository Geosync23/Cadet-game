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
| arrows_check step5 | OK (run by R3, taken from R1) | exit 0, ARROWS CHECK OK (plans/checks-s6-r3.md) |
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

DA6's fix (claude/p5s6-deck 39d69ae: badge, return -> '6-dosi-rack'; reactor -> '6-reactor-1-svc', which is what
panelPlace('6-reactor-1') gives) is the one tested above.

**R1: NO-GO on e0084ca9** until 28c's night 2 arrows are fixed; then step6 x4 again with the fixed check.

## Round 2: candidate 2

- Build: `claude/staging-p5s6` 82b02fb9 (game the same as 78cb7bf7: DA6's 28c fix 673ac4f2 and arrows_check e2442fcc
  in), game sha256 `4a4bed1c6d7b8cb4354d4c4217e970ba2d5b3758a7f0ade48c3c22b159069595` (matched); OLD 0.94.0 6f1915cb
  (matched, not needed: nothing failed). Checks from 82b02fb9. Run 2026-10-27 from 19:28 UTC, two browsers, each its
  own CADET_WORK. Every check: exit 0 and its OK line.

| Check | Result | Key lines |
|---|---|---|
| arrows_check step6 asis | OK | all 13 beats in order; missed 0, stuck 0 (157 s) |
| arrows_check step6 teachoff | OK | the same (156 s) |
| arrows_check step6 track | OK | the same (162 s) |
| arrows_check step6 skiptea | OK | the same; Calder's question by end:find, Day 26 19:35 (160 s) |
| dev_arrow_check | OK | DEV ARROW CHECK OK |
| player_check (with the night part) | OK | PLAYER CHECK OK (708 s) |
| devmode_check | OK | DEVMODE CHECK OK |
| bubble_check | OK | BUBBLE CHECK OK |
| puzzle_check (p6, p7, p8, point) | OK | PUZZLE CHECK OK |
| social_check | OK | SOCIAL CHECK OK |
| talk_check | OK | TALK CHECK OK |
| day_check 4 | OK | DAY CHECK OK |
| day_check 11 | OK | DAY CHECK OK |
| arrows_pointer_check | OK | arrows_pointer_check: OK |
| arrows_check (default parts) | OK | ARROWS CHECK OK (1416 s) |
| arrows_check step5 | OK | ARROWS CHECK OK |

Step 6's beats, every way: the briefing (Day 22 08:15), the Tier 4 test, sleep by day, night 1, engine work night 1
(23:39), the welcome (Day 23 05:45), the badge, night 2, the reactor night 2 (all six m23 arrows led: permit, badge,
tell, reactor, out, badge back), the coil swap (Day 24), the move (Day 25), mentoring and Calder's question (Day 26).

**R1: OK on 82b02fb9.**

### Round 2: taken from R4 (agreed with R4, who didn't start them; 20:33 UTC)

| Check | Result | Key lines |
|---|---|---|
| day_check 26 | OK | DAY CHECK OK |
| day_check 27 | OK | DAY CHECK OK |
| appt_check | OK | APPT CHECK OK |
| saves_check | OK | SAVES CHECK OK |
| stories_check | OK | STORIES CHECK OK |
| clothes_check | OK | ALL OK |
