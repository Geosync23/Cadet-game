# claude/arrows-c: what's in (for BM14)

Kept by AC3 (session_01DiLRzrXgkeoAZCoX1mVJn9) since 2026-10-23 01:51 UTC, before that AC2 (session_015uhdrDuE49CJ8iWWX2SEeP), assembly branch for the Pillar 5 + arrows + fresh-eyes batch 2 build
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

## Merged ahead of their PASS (lead 30, 22:05: "merge now, fix on top; no BM14 until every piece has a PASS")
| What | Branch / commits | Review |
|---|---|---|
| FB1 haul and delivery stops (Cart dock 1, the Folding table), the shelf put-back, a chore's pin whatever is under it | claude/fe-cartdock 228de58 (merge ee420f4), ebf456b (merge 4cdd817), 191bee5 (the galley drop: the tap's line to 1.7 m) | RV8 PASS (a52aad0, 228de58, ebf456b); 191bee5 RV8 PASS |
| FX3 fix 15 (the pin on the thing you need) | 3b7b13d, inside fe-cartdock | RV8 PASS WITH FIXES (one check line) |
| CP4 #38 (the pin on the item; a tap on the pin over the board opens it, read on release) | claude/fe2-tracked f59b471, 016fc65, 1da26e6 (merge f71ab28) | RV8 PASS (016fc65, with fix 15 and FB1) |
| AC2's follower fixes since 483c3da (real taps only at your held job's step, leisure ended, Fault notes, device closed, the tap's ray) | bf27739, afa5900, ac6f66e | RV7 |
| AC2's pop-up queue keeps a training's word | 483c3da | RV7 |
| FX3 fixes 16-18 (with the inspection morning's arrows, direct, off with the queue on) | claude/p5-fix3 a9cabf75 | RV7 PASS |
| AC2 F2: the inspection morning through the queue (level 2) | 5f7e91c | RV7 |
| FX5: p3 trained when Day 5's case is solved before its row opens (24k WORK_MECH.p3.open) | claude/p5-fix5 c5eb7119 (cherry-picked by AC3, e3fb801) | RV9 PASS |
| AC3 follower: an urgent career arrow ends your work; stay in a training meeting's room until it starts (FX4's diagnosis) | 8dd0304 | RV7 PASS |

Clash notes: ixJobStep's make line keeps FX2's scan-first rule with FX3's lathe pin.

## The teaching arrows switched on, and the last pieces (AC3, 2026-10-23)
| What | Branch / commits | Review |
|---|---|---|
| The teaching arrows ON for 0.92.0 (the user via lead 30): POINT_ON + GUIDE_ON true; the arrow checks make their own switched-off copy | e3c7c18, device_check 764438d | RV7 |
| Teaching arrows Off keeps a lesson's watch arrow (T2 `everyday`); arrows_check `teachoff` | f8ed852 | RV7 (lead 31's call) |
| FX4 m7 at 'ask' with the queue off + Calder's "Wait here" | claude/p5-fix4 fc2e1c6 (merge 3d6046a) | RV9 PASS |
| Check-side fixes for the arrows being on: interactions_check Game wrapper (clock in on taking a test job, pop-ups at once), intro_check (pilot's line from the queue; the solo job under Zeke's meeting arrow) | 8eb5715, fcd3df0, fdd1540, 34da38f, 7989742, 7d97d53 | RV7 (whole merge) |
| FX3 fix 19 (a tap at the pin over someone is your job) + its interactions line | claude/p5-fix3 518ee9e, adda4fe (merges 1569810, 8ab6089) | RV7 PASS |
| DV1 Dev mode's career arrow | claude/dev-career-arrow 9f51257 (merge 5f6a19c) | RV10 PASS |
| FB1 Folding-table test fix; the stale-line guard + its fix | 8438e7f (cc4a5c2), bd291e4 + e19625c (a6213a7, b26da80) | FX4 PASS |
| FX5 the arrival-night call-home booth arrow (3 commits) | claude/booth-arrow 771c9ff (merge a2cd3cd) | RV10 PASS |

**Final tip named to BM14: 7d97d538** (lead 31, 2026-10-23 ~08:40 UTC). On it: check_fast OK; arrows_check week guide OK and
week guide teachoff OK (every lesson m1-m7, p3, m2, m6; stuck 0); intro_check OK; cadet_test vs pre-switch c14a799d ALL IDENTICAL;
interactions_check one FAIL, FB1's coverage line "over the garden in some" (all 60 taps did their stop; lead 31: coverage, FX4
makes it deterministic, test-only, BM14 takes it on top). Not in arrows-c: CTT3's controller_check fixes 7f5b13d1 (BM14), tip-clear.

## Checks to run on the tip
check_fast, cadet_test (alone), arrows_check queue / shift guide / week guide, arrows_d_check, arrows_f_check,
arrows_pointer_check, interactions_check, player_check, intro_check (--firsts), mech_check fx3.
