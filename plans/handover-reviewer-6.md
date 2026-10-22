# Handover: RV6, reviewer (arrows E, F3/F4, D; DS1's day-start and bunk-early)

Written 2026-10-22 ~17:50 UTC by RV6 (session_018Jzc4LeoHvuahsS7VHAzn3, about 55% memory). Lead: **lead 29**
(session_01A9rNreAGVbsY1HgPucDMA7; lead 28 session_01S7AdxK1ZyXiEFowP3k5gng before). Read CLAUDE.md, DEV_NOTES
("Rules that keep it working", "Testing"), plans/testing-guide.md, then this.

**Role:** reviewer. Never edits the game. Notes only, on branch `claude/review-arrows` (push only there). Each verdict
goes to the builder and the lead with send_message (plain words, numbered list, PASS / PASS WITH FIXES / FIXES NEEDED).

## Verdicts given (notes in plans/)
| What | Tip | Verdict | Notes |
|---|---|---|---|
| Arrows E, training arrows T1-T3 (AR1) | 14cffba | FIXES NEEDED | review-arrows-e.md |
| E, AC1's fixes | claude/arrows-c d99a9e50 | PASS | same file |
| Start at Day N (DS1) | claude/day-start 64583ba1 | FIXES NEEDED | review-day-start.md |
| Day-start fixes | 1d3f76c3 | PASS | same |
| Arrows F3/F4 (AC1) | 1f2ce27d | FIXES NEEDED (item 2 later withdrawn: my probe's mistake) | review-arrows-f.md |
| F3/F4 fixes | 3519abab, then 5557122e | PASS, PASS | same |
| Bunk too early (DS1) | claude/bunk-early 6b8bb392 | PASS (two word notes) | review-bunk-early.md |
| Arrows D, shift chain (AC2) | claude/arrows-c 4ef580e | PASS (three small notes) | review-arrows-d.md |

## Loose ends (for the lead to route; none are mine to fix)
- E item 5 / D: trainTell's direct arrow still beats T1 when no job is tracked; moves with D after FX1's tip (AC2).
- Rounds' own direct arrow "Take your first round at the job board" (24a) and the burst pipe after the follow both sit on
  the board / the vent while you hold another job: the "another job in hand" pattern (F1 / FX3 / FX1).
- The rec deck: the climbing holds' arrow pin sits on the Climbing wall; tapping what's under the arrow starts a climb
  (AC1 reported it to lead 28; not filed by me).
- D's notes 1-3 (held-first untested, S9 on a drop, S6 during meetings) with AC2.
- bunk-early's two word points with DS1 / the writer.

## How I tested (all in the scratchpad; copies of the probes are in plans/review-arrows-*/)
- Builds: `git show TIP:starship-cadet.html > b/x.html`; an "on" copy replaces `const POINT_ON = false;` with true;
  GUIDE_ON is switched on at run time by arrows_check's `real_game` (its `GUIDE = True`).
- **cadet_test strictly alone** (no other browser), base vs tip: ALL IDENTICAL every time this session.
- check_fast on a tip: a `git worktree add --detach` of it, then `bash check_fast.sh` there with CADET_WORK=/tmp/cadet-work
  (it tests the working tree's file, not an argument). Needs acorn and three in /tmp/cadet-work (testing-guide 2).
- Mutants: RV2's `mutants.py` (copy in plans/review-arrows-d/mutants.py, with my ae_/ae2_/af_/ad_/be_ sets). Put the
  check and cadet_test.py in a folder; the check must keep its own file name (devmode_check finds cadet_test by it).
  `MUT_CHECK=arrows_f_check.py python3 mutants.py GAME.html CHECKDIR CLEAN.log name ...`.
- Play probes: `p_train.py` (a day, arrow / queue / stage at each change), `p_meet.py`, `p_inc.py` / `p_inc2.py` (real
  screen taps) / `p_inc_off.py`, `p_scan.py`. They exec arrows_check.py up to `GUIDE = 'guide' in` and reuse its Page,
  Follower and real_game; pass the matching tip's arrows_check.py.
- Two browsers at most at once, each with its own CADET_WORK (mkdir test; symlink three).

## Gotchas
- **The follower is not a player.** It taps the item nearest the pin: on the rec deck that was the Climbing wall (a
  climb, not the job). Before calling something stuck, re-check with a real screen tap at the pin (`page.mouse.click`
  at the projected point), as p_scan.py / p_inc2.py do. My F3/F4 item 2 was this mistake.
- `pointNow()` returns the pointer's id (a string), not an object; `POINT.aim` is the element.
- An arrow on a crew member (`crew:` goal) can stall the lesson: the player parks beside or taps on the person; both T1
  (Zeke) and F4's follow (Calder) did. Point at where they're going.
- arrows_check.py is on claude/arrows-plan / arrows-c, not integration b9f053ba or earlier (day_saves.py needs it).
- Background jobs over 10 minutes: run with run_in_background and wait on the log's exit line.

## Open questions for the user
None of mine.
