# Handover: RV23 (reviewer: Step 6 and live patches), 2026-10-27

**Role:** reviewer, from RV22. Lead: lead 42 (session_01GKuymjnCHnpwDqB94PVwmV; send_message, priority "next"; took over from lead 41 at 13:58, confirmed by lead 41). My session:
session_01GKuymoDm1XbC5G8TvaCNLr. Notes-only branch `claude/review-rv23`; full log and verdict table: `plans/review-rv23.md`.
Never change the game or push to builders' branches. Verdicts go to lead 42 and the builder (PASS / FIXES NEEDED, MUST vs should, sha).

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
Done at the handover (14:45): PZ6 12afb4a PASS, PZ6 91710ce PASS, MA6 db56362e PASS, N6 992a4b0 off identical, W7 36e8cf5a off
identical (not played live). All sent to lead 42. RV24 (session_01GKuymnJuoJTWnmYunbN7EP, claude/review-rv24) takes over:
1. W8 claude/p5s6-promo4 bd13809 then eee654d (28f Calder's question, mtCasePoint, worksEscort skips p5nEscort on a training/test job):
   check live that Calder still walks to a seated player for the Tier 4 offer and night.on after the worksEscort change.
2. Basil's mentoring day (S6-7) live at 390x844: my mt_play.py used devmodeSetCareer(26, DM_BEATS 'mt') inside devmodeRun and stayed on
   Day 0 (the preset didn't take): find the right Dev call (devmode_check's t4beats loads presets) before playing.
3. Day 22 on merged staging (7bc997eb or c477e525): briefing 08:30 (m21), night.on 09:15-10:00 (Calder waits at m21Door with m21), Tier 4
   test 09:30. Seated in the lounge skipping the briefing, Calder only set off at 10:01 and night.on came by notice. Play Day 22 the way a
   player would (to the briefing, Calder at the door, then the test) and judge whether the three beats fit together.
4. DA6 claude/p5s6-deck 88377cfa + 31ad2f0e (night 2; the m23 arrow my should found; controller m23): cadet, controller m23, and
   interactions_check (it touches 15b's ixChoreLast and section 14's doorOpenFor).
5. The 0.94.0 Tier 3 offer live with the escort fix: p3_play.py on Day 15 found the offer already made during the skip; set it up
   without the skip (or accept: the same fix is proven live on the Tier 4 offer and night.on).

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
