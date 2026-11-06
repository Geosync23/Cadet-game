# 0.99.7 round 0997b (candidate 2): share R2 (2026-11-06)

- Candidate 2: claude/staging-0997 c052cc8, game sha256 1b17203d4281afa28485d7ba05f5afe829931169888d392d97ef5e4f61a0bff9 (matched). Check files from c052cc8.
- OLD: 0.99.6 d7ad4c58, f6ff5ec1...db8a8. Build master BM26, lead 50. Candidate 1's record: plans/checks-0997-r2.md.
- Setup as candidate 1 (two browsers at most; own CADET_WORK /tmp/work-r2, /tmp/work-r2b).

## cadet_test OLD BUILD (alone)

exit 1, `DIFFERENCES FOUND`; `DIFF state ['mem', 'calls', 'tris']` only; `errors A [] errors B []`; taps the same.
Every NEW picture is pixel-identical to candidate 1's NEW picture (0 px in all 15 views), so the differences and their
causes are exactly candidate 1's (plans/checks-0997-r2.md, pictures in plans/checks-0997-r2-cadet/):

| View | px | What differs |
|---|---|---|
| a_start | 8424 | hair (CH_HAIR), soles (CH_SOLE) |
| b_wander10s | 7273 | the same |
| c_rotated | 6133 | the same |
| d_wallslow | 7085 | the same |
| e_night | 2600 | the same; Fonseca 0.1 m over in a bunk (CH1) |
| f_noshadow | 5760 | hair, soles |
| g_nocrew | 665 | the player's hair and soles |
| h_crewback | 10617 | hair, soles |
| i_tap0 | 9027 | hair, soles; tracker ring (TP1); Pell 0.2 m (TRAD997: the Spice supper move, by design) |
| i_tap1 | 23361 | hair, soles, tracker ring; crew elsewhere from Day 2 ~07:45 (TRAD997), bubbles follow |
| i_tap2 | 20920 | the same |
| i_tap3 | 57102 | the same |
| i_tap4 | 8679 | the same |
| j_steer1 | 32167 | the same |
| j_steer2 | 13637 | the same |

## Result: running
