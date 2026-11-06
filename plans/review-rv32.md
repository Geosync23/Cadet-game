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

### 1. CH1 batch A (claude/p997-chars 3d07e66): notes 37, 35, 10, 1
Game sha256 180e78d4f891df4362c33aa050a071dfa24eecf8965a00e385a0da41f3b86179 (matches). Switches CH_SOLE_ON, CH_POSE_ON,
CH_RELAY_ON, CH_HAIR_ON (CH_SEAT_ON declared, note 4 not built: batch B). Sections: 4d (1 line), 8 (slot), 8b (1 line), 8c (1 line).
- Off: cadet_test 0.99.6 vs 3d07e66 ALL IDENTICAL.
- On (all four): cadet_test vs 0.99.6: only triangles and the pictures differ; paths, collisions, crew walks and taps the same; no page errors.
- Note 1 hair (plans/rv32-probes/ch1_look.py, magenta skin, close crew and crowd, 5 views; results/hair_sheet-3d07e66.jpg):
  skin showing through hair (magenta pixels) in 0.99.6: short/buzz/curls/bun/ponytail/long, worst on crowd buzz (5400 px
  from the game's angle) and curls (3286). On: 0 for every crowd view; close crew at most 19 px (buzz and bun, from straight above).
  The crowd's near caps come out about 8% fuller than before (the cos correction plus the pad); looks fine to me.
- Note 37 soles (results/feet_sheet-3d07e66.jpg): the flat plate is gone, the rounded boot still meets the floor (no float).
- Note 35 pose (ch1_seats.py, the rec deck's auditorium seats and beanbags filled with 'sit:slump'; results/seat_sheet-3d07e66.jpg):
  0.99.6 forearms held out in front (the bike handles); on: arms down, hands on the seat by the hips. The hands-behind-head
  variant unchanged. Nothing seen through the seat or beanbag.
- Note 10 relay cabinet (ch1_relay.py; results/relay_sheet-3d07e66.jpg): 0.99.6 the cabinet's back (z 9.87) pokes over the
  hull rim from outside; on (z 9.08-9.52) it stands inside. Fault lamp: lamp z moves with the cabinet (in front of its face by
  0.06 both builds). Junior wing cabinet (closet k) checked too: already inside, unchanged.
- check_fast on a copy with all four switches on: QUICK CHECK OK in 337 s (deck_check's draw calls included).
- Verdict: PASS for notes 37, 35, 10, 1. Note 4 (CH_SEAT_ON) still to come in batch B.
