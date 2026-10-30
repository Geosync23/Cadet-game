# Handover: build master 9 (BM9, session_01W4FMKvz4gV1LWn5jnLaQVT): PAUSED

**Paused** on the user's request via lead 19 (2026-10-19 ~13:23). Nothing runs; nothing more is pushed to `claude/rec-cand-s1` until the lead says so.
**Lead:** lead 19, session_01FsGspstkG61e9AWadSi36y. **Check runner:** CR2, session_018xWmWkrtNWudZUgXygkW1u (paused too). **Rec engineer:** RC, session_01RzT48sAzLqDhsRzzNNdXU3 (lead 19's fix seat; the lead passes the pause). R7 reviewer and BM8 have stopped (notes: `claude/reviews-r7` plans/handover-reviewer-r7.md, plans/handover-build-master-8.md).
**Scope (lead 19):** finish 0.64.0 (rec deck switched on), then stop. The lead publishes the green hash as a NEW artifact "Starship Cadet Rec Deck", never over the main link.

## Builds
- **0.63.5 final:** `claude/p5-cand-s5` 38dcac4 (game identical to be3d7ee). Done (BM8).
- **0.64.0:** `claude/rec-cand-s1`:
  - 3add6bf: be3d7ee + rec-works f319ab3 → rec-crew 9dfe971 → writer-rec a095799 → rec-works 87e3c5f (REC_DECK = true). R7 PASS on the merges. My own blind combine (same order) gives a byte-identical game.
  - 9bc151b: BM8's handover note + tools (no game change).
  - 50d55ef: "The rec deck's closed till six." (discAsk's toast + its comment; R7's find). R7 PASS.
  - 6e20c89: device_check.py only (check fix, below).
  - 7a3f0cc: disc_check.py only (check fix, below).
  - This note on top.
  - **Game file is the same from 50d55ef to the tip.** RC's game fix (not pushed at pause) goes on top.

## Results (game = 3add6bf unless it says 50d55ef; 50d55ef differs only by the toast text)
| Check | Result | Notes |
|---|---|---|
| node --check, duplicate top-level names | OK | |
| cadet_test vs 0.63.5 | DIFFERENCES, explained | a-d 0 px; e_night on: big. Dormant proof: 0.63.5 relabelled 0.64.0 vs 3add6bf with REC_DECK=false = 0 px on all 15 shots; only state diff: 2 Deck 4 item texts (W3's "seven decks" spine ladder + directory with R, not gated on REC_DECK; fine with the deck on, note for DEV_NOTES). ON vs OFF reproduces BM8's numbers exactly; g_nocrew differs by crew speech bubbles + one crew prop (the ship sim runs differently with the rec system and rec visits). |
| deck_check | OK | BM8 and BM9 |
| lines_check | PASS (0 errors, 5 warnings) | 3add6bf and 50d55ef |
| mech_check | OK | BM8 |
| interactions_check | OK | 3add6bf (BM8) and 50d55ef (BM9) |
| device_check | OK with 6e20c89 | Was FAIL x2 (heads-up queue): the rec tradition "Float hour" is day 3 21:30, the very minute the check stages its appointment. Game right; the check now stubs traditions in the two appointment-only blocks. OK on 50d55ef and on 0.63.5's game. |
| disc_check | ALL OK with 7a3f0cc | Was FAIL "just the one crew member on the rec deck": crew now visit at 19:00 on their own. The check now asks that the one you asked is there. OK on 50d55ef and on 0.63.5's game. |
| machine_check | **FAIL → RC** | 'caches cleared' wear differs + traced faults not the same twice. Cause: RA's recVisit (day planner, ~line 10051) calls recShutAt → MACH_HIST, so a day's plan depends on when it was planned (plan → use → wear → record → plan). Off copy OK. `const sh = null` there passes both, but tips 'steady player 6.1 jobs/shift day (want 3-6)'. Lead 19: proper fix by RC, no band change. |
| career_check | **FAIL → RC** | 'busy: Relied on before Day 5' (busy xp by Day 4: 43 on vs 37 off; the 16 rec machines add jobs). Lead 19: recheck on RC's hash; if still failing, rec machine jobs give half career xp (one named constant), band unchanged. |
| day_check 0, 6, 7 | OK (CR2, 3add6bf) | |
| day_check 1, 2, 8 | **FAIL → RC** (CR2) | only 'work: volkov-maeve 476/480': her rec round's 2 lift rides (10:26-10:28, 10:58-11:00) are planned as 'commute' mid-shift. Every weekday. Lead 19: RC counts them on-shift in the planner. |
| day_check 3, 21 | stopped part-way at the pause (CR2) | |
| day_check 4, 5, 14, 28 | not run (dropped to wait for RC's hash) | |
| player_check | stopped at the pause (371 s of ~35 min, 50d55ef) | one FAIL already printed, not placed: 'tradition posts name it, not its id (reviewer 1e): None' (no tradition post found in the news feed's window). Rerun in full; place it with the REC_DECK=false copy. |
| events, intro --week, join, food, clothes, smoke, newgame, leave, bubble, tiles, path, arc | not run (CR2 had queued them; paused first) | CR2's note: `claude/p5-cand-s4-checks` fe3ff05 plans/cand-0640-cr2.md |

## To do when work resumes
1. RC's hash (machine fix + Maeve's rides + maybe the career constant): R7's successor reviews it; prove dormant identical (cadet_test 0.63.5@0.64.0 vs the tip with REC_DECK=false: 0 px).
2. On RC's hash, rerun: machine, career, day 0-8 + 14/21/28, events, deck, cadet (vs 0.63.5 and the dormant proof), player (place the tradition-posts line), plus whatever of CR2's set didn't finish. Two or three checks at once at most.
3. DEV_NOTES 0.64.0 row (pieces, hand merges, check fixes, results; W3's ungated "seven decks" texts), plans/cand-0640-results.md, push, green hash to lead 19.

## Setup (to rerun)
`pip install playwright`; three r128 in /tmp/cadet-work/three; `ln -sfn <scratchpad>/cw /tmp/cw`; copy plans/build-master/* to /tmp/cw/bm; a worktree of claude/rec-cand-s1 at /tmp/cw/wt64; `WT=/tmp/cw/wt64 TMO=2700 bash /tmp/cw/bm/bm8/q3.sh GAME.html TAG check...` (one line per check in /tmp/cw/logs/summary.txt). Off copy: `sed 's/^const REC_DECK = true;/const REC_DECK = false;/'`. Never pkill -f a pattern in your own command line.
