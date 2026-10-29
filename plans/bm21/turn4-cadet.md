# RB1 turn 4 on staging-099: the cadet pictures (BM21, 2026-10-29)

Merge: staging-099 536748f7 + claude/opt-098-render e7bce5a9 = c5f52108 (game sha256 8a0cbb86...a7c4, matches RB1's).
cadet_test 536748f7 vs c5f52108, run strictly alone:

| Shot | Pixels different | Largest | What |
|---|---|---|---|
| d_wallslow | 8 | 18 | the user-approved corner pixels (RB1's turn4-pixels.md) |
| i_tap2 | 1 | 24 | the same kind, as RB1 reported |
| a_start | 14812 | 153 | only the speech bubble ("Planted mine in a straight line.") a few pixels apart; the 3D scene is identical outside the bubble's box (turn4-a_start-bubble.png: before, after, changed pixels in white) |
| the other 12 | 0 | 0 | |

The bubble follows its speaker on real time, so its exact spot can vary between runs; an earlier run of the same pair had a_start at 1-level noise only. 536748f7 against itself: ALL IDENTICAL. State: mem, calls, tris differ (geometries 422 -> 414), as expected.
