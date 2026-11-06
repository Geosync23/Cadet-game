# 0.99.7 full round: share R2 (2026-11-06)

- Candidate (NEW): claude/staging-0997 7fd8f6b (build turn 363107d), build 0.99.7, game sha256 b14421f82e04602cd608505756ddb8fb05bea4571af813d8e345424ebcd1cf7d (matched). Build master BM26 (took over from BM25 ~13:00).
- OLD: 0.99.6, main = claude/integration d7ad4c58, game sha256 f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8 (matched); names_check on OLD OK.
- Setup: playwright (pip) with CADET_CHROME=/opt/pw-browsers/chromium; three.js r128 and acorn 8.12.1 (npm pack) in my own CADET_WORK (/tmp/work-r2, /tmp/work-r2b); numpy, pillow; two browsers at most.
- Share (plans/round-0997.md R2): intro_check (whole), --dinner, --firsts, perf_check BUILD OLD, cadet_test OLD BUILD, path, arc, lines, lines --day, p926, day_check 0, 1, 5, 7, 21, 22, arrows endgo, pf_f1_same OLD BUILD 10, fresh_walk BUILD 3.

## Result: running

## fresh_walk: how it is judged (BM25, 2026-11-06)
Run: `python3 plans/rv32-probes/fresh_walk.py BUILD 3 $CADET_WORK/fw.json` (Days 0-3, sleep 22:30). It prints no OK line; pass when all five hold:
1. Day 1: the briefing meets (d1-briefing:met) and the Chief stays until it ends.
2. The Day 1 arrow leads to the Works bay before 08:50, then to the clock.
3. Day 2's 08:45 solo meeting and the 18:00 booths each get an arrow and happen.
4. No page errors.
5. The follower is never stuck for an hour.

## cadet_test OLD BUILD (alone)

exit 1, `DIFFERENCES FOUND`; `errors A [] errors B []`; taps the same; `DIFF state ['mem', 'calls', 'tris']` only (new
geometry); paths, collisions, walkers and the seed the same. Every view differs (log and side-by-side pictures, OLD | NEW |
the differing pixels in red, in plans/checks-0997-r2-cadet/):

| View | px | What differs |
|---|---|---|
| a_start, b_wander10s, c_rotated, d_wallslow, f_noshadow, h_crewback | 5760-10617 | heads (hair caps, CH_HAIR) and feet (no sole boxes, CH_SOLE) on every person |
| e_night | 2600 | the same; plus Fonseca 0.1 m over in a bunk (CH1, by the bisect below) |
| g_nocrew | 665 | the player's hair and soles only |
| i_tap0 to i_tap4, j_steer1, j_steer2 | 8679-57102 | hair and soles; the Schedule tracker button's ring (TP1); and from Day 2 ~07:45 the scheduled crew elsewhere, with their speech bubbles (below) |

The player is in the same place at every view, at the same speed (fitness lower: MV_FIT). cadet_test's own walker check
covers `walkers`, not the scheduled crew (DECK_CREW), so it doesn't flag the crew. Their positions per view:
plans/checks-0997-r2-cadet/crew_positions.txt.

Bisect (copies of NEW with switch lines set false; DECK_CREW compared at every view):
- every 0.99.7 switch off: the crew as OLD exactly;
- CAL997_ON off alone: the Day 2 drift stays (not the calendar);
- CH1's five off: only the Day 1 night 0.1 m goes (CH_SEAT etc., by design);
- TP997, TRAD997, GAMES997 and EV997_* off together: the whole Day 2 drift goes. Split into the four: running.
