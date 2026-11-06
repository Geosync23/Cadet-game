# RV32 review notes (0.99.7 playtest patch)

Reviewer RV32 (session_01GKuymkDX3gviqiGJcKLWuS), reports to lead 49 (session_01GKuymjjreuZtZeDMBX79xn).
Base: claude/integration d7ad4c58, game f6ff5ec1...db8a8 (0.99.6). Plan: plans/patch-0997.md on claude/lead-49.
Reviewing: CH1 (claude/p997-chars), MV1 (claude/p997-move), TP1 (claude/p997-tips), CR1 (claude/p997-career), JB3 (claude/p997-jobs).

For each build: does it do what the user's note asks (probed in the real game, phone size where it matters); switch off =
identical (cadet_test.py vs 0.99.6); switch on: the area's checks plus check_fast; sections touched (tools/section.py --diff).

## Setup
Kit ready 2026-11-06: playwright, numpy, pillow; three r128 and acorn 8.12.1 in /tmp/cadet-work; CADET_CHROME=/opt/pw-browsers/chromium.
Smoke test: cadet_test 0.99.6 vs itself ALL IDENTICAL (64 s).

## Lead 49's rule for this round
For every week-1 note (tips 6/9/11, the Day 1 briefing, the Day 8 promotion, week-1 jobs): probe from a fresh save with
the intro ON, following the arrows like a player (a 0.99.5 fix passed with the intro off and failed on a fresh save).
Tool for it: arrows_check.py's Follower walker (see plans/rv30-probes/arrow_walk.py on claude/review-rv30).

## Verdicts
(none yet)
