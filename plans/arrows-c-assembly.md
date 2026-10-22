# claude/arrows-c: what's in (for BM14)

Kept by AC2 (session_015uhdrDuE49CJ8iWWX2SEeP), assembly branch for the Pillar 5 + arrows + fresh-eyes batch 2 build
(lead 29, 2026-10-22). Base: claude/integration 2b4a05db (0.64.15). BM14 merges arrows-c onto 0.91.0 (IM1 has the
resolutions). History is merge commits and `cherry-pick -x` only, never rewritten.

## Arrows plan pieces (all switched off: GUIDE_ON / POINT_ON)
| Piece | Who | Review | Where |
|---|---|---|---|
| B, the arrow queue | AR1 | RV2 PASS | 15b slot |
| C, the panel pointer, Settings "Teaching arrows", the lift pointer | AC1 | RV2 PASS | 19 slot (+ 15b ixBoard data-job) |
| E, the training arrows T1-T3 | AR1, AC1 | RV6 PASS | 15b slot |
| F3 (the scanner, Fault notes), F4 (the burst pipe) | AC1 | RV6 (fixes done) | 24k slot, 24f |
| The training watch arrow (direct, queue off) | AC1 | AR2 PASS (90992e66) | 24p slot |
| D, the shift chain S1-S9 | AC2 | RV6 PASS (4ef580e); later commits RV7 | 15b slot (+ 15 clockRmPoint, 15b ixWorkStep, 24p trainArrow) |

## Fixes merged (switched on)
| What | Branch / commits | Review |
|---|---|---|
| FX1 arrow and tracking lifecycle | claude/p5-fix1 a34f466 (merge 82b92a9) | AR2 |
| FX2 drill, scanner job, tuning words, calibrate, dropped part | claude/p5-fix2 cc2bb2b (merged by AC1) | PR9 |
| FX3 lift, burst pipe, small lessons, hauling, fixes 10-14 | claude/p5-fix3 to 2cdc1df (merge 00f4436) | PR9, RV7 (fix 14) |
| The job board's Take it for rounds and hauls (BOARD_KINDS) | AC2 6610dc7, 78fef90 | RV7 PASS WITH FIXES (done) |
| The drill arrow is FX2's own line; S9 "reputation down"; boardEmptySay waits through a meeting / training / dialogue | AC2 6610dc7 | RV7 |
| The tea arrow clears when tea is over | AC2 695cf6e | RV7 |
| The job arrow rests after clock-out | AC2 86faa86 | RV7 |
| arrows_check follower fixes (held job first, floor at the pin, stand up, real taps at job pins) | AC2 c26f194, 7ff2c27, 69d1ed9, 86faa86, 5160b81 | RV7 |

## Fresh-eyes batch 2
| Item | Branch / commits | Review |
|---|---|---|
| DS1 #27 (words once on a card) | claude/fe2-player 1dd4f56 (merge 18eb5f8; includes 418ff16, 88df589) | PASS |
| CP4 #24 (a row for tomorrow), #41 (the row followed is highlighted) | claude/fe2-tracked 251d978 (merge 7741248; includes 279b94f) | PASS |
| FX2 #36 (Day 1 tracked Clock in stays up), #48 (any Tea corner chair), player_check tea part, RV8's #36 note | cherry-picked d59e8e9, 493b84e, 421838e, ffdbb8c (9396b1c, 891837b, ca50bc3, 5f755e4) | RV8 PASS |

Cherry-pick notes: d59e8e9's intro_check change taken as its own lines only (`clock_tracked` and its call); 493b84e's
player_check change taken as the tea part only (its context carried a fix-eat part not on this branch).

## Waiting (merge when it passes)
- FB1 claude/fe-cartdock (5df8492: haul stops under a machine or by the drop; RV8).
- FX3 p5-fix3 fixes 15, 16; the inspection arrows; the climbing wall (RV7).
- CP4 #38 (f59b471: the pin on the item; a tap on the pin over the job board opens it; RV8's 1-in-3 pin miss).

## Checks to run on the tip
check_fast, cadet_test (alone), arrows_check queue / shift guide / week guide, arrows_d_check, arrows_f_check,
arrows_pointer_check, interactions_check, player_check, intro_check (--firsts), mech_check fx3.
