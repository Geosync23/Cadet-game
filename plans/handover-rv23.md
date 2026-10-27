# Handover: RV23 (reviewer: Step 6 and live patches), 2026-10-27

**Role:** reviewer, from RV22. Lead: lead 41 (session_01GKuymjWR1dqfbCw1MyEP9j; send_message, priority "next"). My session:
session_01GKuymoDm1XbC5G8TvaCNLr. Notes-only branch `claude/review-rv23`; full log and verdict table: `plans/review-rv23.md`.
Never change the game or push to builders' branches. Verdicts go to lead 41 and the builder (PASS / FIXES NEEDED, MUST vs should, sha).

Read first: CLAUDE.md, plans/handover-rv22.md (how RV22 tested), then the verdict table in plans/review-rv23.md. User rules for every
verdict: works with a game controller; tons of arrows, obvious progression; key moments are staged scenes, in person first (Mail only
as the record); phones first (390x844); everything new switched OFF must be identical (cadet_test) until it's switched on.

## Builders (Step 6, base claude/staging-p5s6)
W7 (took S6-3 and S6-7 from W6) session_01GKuymjghu82TGWPLR1wTKw, claude/p5s6-promo4. N6 (S6-1 nights) session_01GKuymnDA25R2a5yZGYpaBS,
claude/p5s6-nights. MA6 (S6-2 briefing, S6-6 team) session_01GKuymj1UEDuEYMnG9rmFkc, claude/p5s6-mech-a. PZ6 (S6-8 cases, casePoint,
team-turn-fix) session_01GKuymjrmdGE4vaHHHGkvYF, claude/p5s6-puzzles. DA6 (S6-4 deck, S6-5 engine work) session_01GKuymjJ4sU5hfdU8bH49UW,
claude/p5s6-deck. BM19 (build master) session_01GKuymncYhRTKs8t4byNfdj.

## The big find (cleared)
Calder's "come and find you" escort (worksEscort { mode: 'follow' }) never walked: her goal was your own tile, and a seat's tile isn't
free, so no path and no retry. W7's fix claude/escort-follow-fix cffe8187 (section 10 escortStep: nearest open tile beside you, retry
every 0.5 s). Proven live: W7 de6d5525 (Tier 4 offer) and N6 06b6a158 + cffe8187 (night.on), both seated in the bow lounge.

## Open items (exact state at writing)
1. p3_play.py (the 0.94.0 Tier 3 offer, seated, Day 15, on cffe8187): was running; lead 41 asked for it (the fix in the live game).
2. Queued in /tmp/rv23/s6 lane1.sh / lane2.sh: PZ6 team-turn-fix 12afb4a (cadet vs 6f1915cb, interactions_check, controller team), N6
   992a4b0 (cadet vs a2ef6416), PZ6 91710ce casePoint (cadet vs a2ef6416, puzzle_check point), MA6 db56362e (cadet vs ce113792,
   controller m24). Results land in /tmp/rv23/s6/done.txt (gone if the container is reclaimed: re-run).
3. N6's final Day 22 probe once cffe8187 is in staging (n6_play.py on N6's head with Step 6 on).
4. Basil's mentoring day (W7 S6-7 later turns): play it live at 390x844.
5. DA6 9332d5a1 shoulds: a controller part for M23 night 1; a shot of the job's ring at stop 1.

## How I test
Setup per plans/testing-guide.md section 2 in /tmp/cadet-work and /tmp/cadet-work2 (two lanes, at most 2 browsers on 4 cores). One
worktree per sha under /tmp/rv23/wt-<sha>. ON copy for Step 6: `sed "s/URL_FLAGS.has('p5s6')/true/"` on the P5_STEP6 line. cadet_test
beside another browser can show "renderer noise" or a one-frame start difference: re-run alone. Probes in plans/rv23-shots/ (copy the
probe next to the game file: they exec its cadet_test.py): p4_play.py (Tier 4 offer), p3_play.py (Tier 3), n6_play.py (nights),
p4_diag.py (escort state), d6_look.py (Deck 6), talk_play.py, vb1_play.py, vw_play.py. Gotchas: never `pkill -f <name>` from the
tool shell (it kills your own command, exit 144); a waiter `until ! pgrep -f X` matches its own command line (use a script file);
play() in the probes picks choice 2 (p4_play passes 2 on a 2-choice scene: the scene never ends: a probe bug, not the game).

## Open questions for the user
None from me.
