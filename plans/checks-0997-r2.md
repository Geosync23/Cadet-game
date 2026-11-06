# 0.99.7 full round: share R2 (2026-11-06)

- Candidate (NEW): claude/staging-0997 7fd8f6b (build turn 363107d), build 0.99.7, game sha256 b14421f82e04602cd608505756ddb8fb05bea4571af813d8e345424ebcd1cf7d (matched). Build master BM26 (took over from BM25 ~13:00).
- OLD: 0.99.6, main = claude/integration d7ad4c58, game sha256 f6ff5ec1e4b55c44425d046765d30c8f1173464cad9327913372b579c57db8a8 (matched); names_check on OLD OK.
- Setup: playwright (pip) with CADET_CHROME=/opt/pw-browsers/chromium; three.js r128 and acorn 8.12.1 (npm pack) in my own CADET_WORK (/tmp/work-r2, /tmp/work-r2b); numpy, pillow; two browsers at most.
- Share (plans/round-0997.md R2): intro_check (whole), --dinner, --firsts, perf_check BUILD OLD, cadet_test OLD BUILD, path, arc, lines, lines --day, p926, day_check 0, 1, 5, 7, 21, 22, arrows endgo, pf_f1_same OLD BUILD 10, fresh_walk BUILD 3.

## Result on candidate 1 (b14421f8...cf7d): FAIL, lines_check NEW (K); the rest moved to candidate 2

| Check | Result | Minutes | Key lines |
|---|---|---|---|
| cadet_test OLD BUILD (alone) | exit 1, every difference placed (below) | 1 | `DIFFERENCES FOUND`, errors none, taps the same |
| intro_check (whole) | exit 0 | 48 | `OK` |
| intro_check --dinner | exit 0 | 3 | `OK` |
| intro_check --firsts | exit 0 | 1 | `OK` |
| path_check | exit 0 | 1 | `PATH CHECK OK` |
| arc_check | exit 0 | 0 | `ARC CHECK OK` |
| lines_check | **exit 1, NEW** | 0 | `lines_check: FAIL (21 errors, 116 warnings)`; OLD in its own worktree `PASS (0 errors, 112 warnings)`; errors in plans/checks-0997-r2-cadet/lines.txt (17 new lines over 90 characters: CL1, TP1, the join997 notices, CR1; 4 TP1 lines with the unknown token {item}). Reported 14:40; CL1 fixing |
| day_check 0 | OK (exit not kept: lane restart) | 6 | `DAY CHECK OK` |
| day_check 1 | exit 0 (re-run; the first run was cut short by my lane restart) | 5 | `DAY CHECK OK` |
| day_check 5, 7, 21, 22 | exit 0 each | 5-6 | `DAY CHECK OK` |
| arrows_check endgo | OK (exit not kept: lane restart) | 11 | `ARROWS CHECK OK` |
| pf_f1_same OLD BUILD 10 | F1 OK; fingerprints differ by design | 0 | `F1 checks 23674 mismatches 0 None`, `page errors [] []`, `fingerprints 30 differ 30` (prints `PF F1 SAME FAILED`); proof: OLD vs the candidate with every 0.99.7 switch false: `fingerprints 30 differ 0 []`, `PF F1 SAME OK` (BM26 agreed) |
| lines --day, fresh_walk, p926, perf | not finished: the container restarted 14:39; then stopped 14:42 at BM26's and lead 50's word, to run on candidate 2 | | |

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
- TP997, TRAD997, GAMES997 and EV997_* off together: the whole Day 2 drift goes;
- split, each off alone: **TRAD997_ON (TB6) off puts every Day 2 crew position back as OLD**; TP997_ON, GAMES997_ON,
  EV997_* off alone: the drift stays exactly as NEW.
TB6 explained it (lead 50): the Spice supper move, by design. So TB6's hosted traditions change the crew's plan from Day 2 ~07:45 (not the bunk inspection, which is Wednesdays; which TB6
part not traced). Sent to BM26 and lead 50 (13:5x); BM26's disc_check #25 (Day 2 17:22, one of the pair on court) likely the same cause, not proven by me.
