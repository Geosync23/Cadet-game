# RV32 review notes (0.99.7 playtest patch)

Reviewer RV32 (session_01GKuymkDX3gviqiGJcKLWuS), reports to lead 49 (session_01GKuymjjreuZtZeDMBX79xn).
Base: claude/integration d7ad4c58, game f6ff5ec1...db8a8 (0.99.6). Plan: plans/patch-0997.md on claude/lead-49.
Reviewing: CH1 (claude/p997-chars), MV1 (claude/p997-move), TP1 (claude/p997-tips), CR1 (claude/p997-career), JB3 (claude/p997-jobs).

For each build: does it do what the user's note asks (probed in the real game, phone size where it matters); switch off =
identical (cadet_test.py vs 0.99.6); switch on: the area's checks plus check_fast; sections touched (tools/section.py --diff).

## Setup
Kit ready 2026-11-06: playwright, numpy, pillow; three r128 and acorn 8.12.1 in /tmp/cadet-work; CADET_CHROME=/opt/pw-browsers/chromium.
Smoke test: cadet_test 0.99.6 vs itself ALL IDENTICAL (64 s).

## Verdicts
(none yet)
