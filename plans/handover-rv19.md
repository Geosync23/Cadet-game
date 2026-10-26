# Handover: RV19 (reviewer), 2026-10-26

RV19, session_01V6FDCQp5Ejidi8Chpo2nJG. Hired by lead 38 for 0.93.2; lead 39 from about 18:00. Notes only, branch
`claude/review-rv19` (from claude/integration b957b92d). Never edits the game: builders fix. Written at about 52% memory.

## Verdicts given (each with its sha to the lead, BM18 and the builder)
| Work | Builder | Branch @ sha | Verdict |
|---|---|---|---|
| Bunk inspection (INSPECT_ON) | FX20 then FX20b | claude/inspection 03449ace FIXES NEEDED; 9b7eae69 PASS | PASS. BM18 later found events_check failing with it on (rec-dawn-swim host, Madsen's sleep): I hadn't run events_check. FX20b's fix e45b7fe went to RV18 |
| Save slots (SAVE_SLOTS_ON) | FX27 | claude/save-slots ba6b7b9a PASS; test-only a1df5739 PASS | PASS |
| Promotion beats (PROMO_BEATS_ON) | FX28 | claude/promo-beats bd558a84 / 104420fd FIXES NEEDED; 44a4565f PASS | PASS |
| Storm Saturday (STORM_SAT_ON) | FX26 (from RV18) | claude/storm-sat 402899bd PASS; follow-up 6f19944d PASS | PASS |
| Pillar 5 Step 5 skeleton (P5_STEP5) | B1 | claude/p5s5-skeleton 5957d244 | FIXES NEEDED, M1 check only (bigevents_check guard samples stale with ?p5s5 on); off identical, safe to merge off if lead 39 says so |

Everything is written up, with checks and findings, in `plans/review-rv19.md`.

## Loose ends
- Save slots on a real phone: someone opens the published 0.93.2 page on a phone and taps Download my save, then Load a
  save file with that file (claude.ai's download confirmation needs a person). The page must be published with
  `capabilities: { downloads: true }`, or Download falls back to Copy save as text.
- Non-blocking notes left open: storm stories' asides rotate over 4 lines (one came 3 times in 30 min); the join toast
  shows twice for every joinable tradition (old); "Works reputation down: New officer" on promotion day (old, xp reset);
  the pip ceremony closes at its length if you never come (old); stormSatDay is cached per page.

## My tools (on claude/review-rv19)
- `plans/rv19-probe-inspect.py GAME_ON.html DAY [bunk|follow]`: the inspection walker's room and distance to its target
  every ship minute, every worksSay/toast and the Mail. `follow` puts you in the walker's current room.
- `plans/rv19-slots-check.py OLD.html NEW.html SERVE_DIR`: a real 0.93.1 save (Playtest and Dev) opened by the new build
  on one http origin; broken slot keys; bad files; a thin file that passes saveOk.
- `plans/rv19-promo-live.py GAME.html SERVE_DIR SHOT_DIR`: Dev mode on a real Dev save through the Tier 2 test, the
  result, the pip and the cabin walk, logging toasts, notices, Mail, bubbles, cards and shots.
- `plans/rv19-storm-live.py GAME.html SERVE_DIR SHOT_DIR`: Friday 18:00 to the storm stories on Day 13.
- Pattern for all: instrument the build like cadet_test (exec its top half), hook the UI functions by wrapping them
  (toast, deviceNotify, worksSay, bubbleSay, mailSend, dialogueShow), step real frames with the draw skipped but the last.

## Gotchas
- At most two browsers at once on 4 cores, or slow checks (interactions, arrows, fridays: 30-45 min each here) time out.
- Never return a three.js object (or a Map holding them, e.g. `[...DRESS.on]`) from page.evaluate: Python's memory climbs
  to 12 GB and the process is killed. Return ids (`[...DRESS.on.keys()]`).
- `pkill -f <pattern>` matching your own command line kills your shell: kill by pid.
- Dev mode's clock skip past 12:30 "excuses" a workday, which can move career beats to the next day (Dev only).
- A Bash wait longer than 10 minutes goes to the background; use run_in_background with an until-loop.
- Run events_check whenever a change touches the planner (section 14): my inspection miss.

## How I review
Read the diff by section (`tools/section.py --diff`), then: cadet_test off vs the base (and as pushed), check_fast, the
checks for the sections touched (events_check for any planner change), then play it at 390 x 844 with a probe and
screenshots against the user's rule. Verdicts PASS / FIXES NEEDED with M (must) and S (should) items, to the lead, the
build master and the builder with the exact sha. Offload slow checks to idle check runners when the lead says so.
