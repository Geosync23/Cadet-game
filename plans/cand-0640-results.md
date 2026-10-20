# 0.64.0 candidate results: the rec deck switched on (build master 10, session_01KpcQGJvrAz57dmKp6AFg4w)

Branch `claude/rec-cand-s1`. Lead 20 (session_019UJSCUCdtC1kTpYiABWKhs); rec engineer RE20 (session_019auXkZkQG3gnNjmArAauLx) owns the game changes; reviewer R8 (session_01GdhqdLeZuGFQSTX7RL92U5, notes `claude/reviews-r8` plans/reviews-rec-r8.md). Earlier work on this branch: BM8 (combine 3add6bf), BM9 (50d55ef, the device/disc check fixes, plans/handover-build-master-9.md), CR2 (`claude/p5-cand-s4-checks` plans/cand-0640-cr2.md).

The candidate is named 0.64.0 (the rec deck combine); its game file says **build 0.64.2** (RE20's two fix rounds on top: DEV_NOTES rows 0.64.1, 0.64.2).

## What's in it
- 3add6bf: 0.63.5 final be3d7ee + rec-works f319ab3 → rec-crew 9dfe971 → writer-rec a095799 → rec-works 87e3c5f (`REC_DECK = true`). R7 PASS. Hand merges: plans/handover-build-master-8.md.
- 50d55ef: "The rec deck's closed till six." (R7 PASS). 6e20c89 device_check, 7a3f0cc disc_check (check-only; BM9).
- e71388f (BM10, check-only): player_check's 'tradition posts name it, not its id' line (below).
- 1eeb99c: merge of RE20's `claude/rc-wip` bf71e7a (0.64.1 determinism of the rec plans, Maeve's rides on-shift, R8's machUseDay speed fix, the rec deck cap from the ride down, the climbing wall's queue + interactions_check case; 0.64.2 item D, Tracked on phones under the needs strip's left end). **R8: PASS** (cadet_test vs cf55b35 ALL IDENTICAL on and off; interactions OK on and off).

## Before RE20's hash (game = 50d55ef, checks of e71388f)
intro --week, join, food, clothes, smoke, newgame, leave, bubble, tiles, path, arc: all OK. player_check: PLAYER CHECK OK (23 min alone).
- **Placed: 'tradition posts name it, not its id (reviewer 1e): None'** was the check's, not the game's. The real news bank always has a tradition line, so the check's stand-in post (`tntoday`) is never added, and it fell back to "a 'Today aboard' post among the last 40 kept". With the deck on, the rec traditions (Float hour, Wall night, paddle club…) take the feed's tradition slots and every one has a bank line, so no fallback post was in the window. Every post did name its tradition ("A ship tradition today: birthday."). With REC_DECK=false the fallback happened to be in the window (True). The check now reads every tradition post of its 14 days: none shows a hyphenated tradition id, and some post names a tradition. True on 50d55ef, its REC_DECK=false copy and 0.63.5's game.

## The round on 1eeb99c (game build 0.64.2), each check in its own CADET_WORK, 3 at once
Judged by each check's printed last line, not its exit code (deck_check, machine_check and day_check exit 0 when they fail).

| Check | Result |
|---|---|
| node --check, name_check (duplicate top-level names) | OK, NAMES OK (3356) |
| **Dormant proof:** cadet_test 0.63.5 (relabelled 0.64.2) vs 0.64.2 with REC_DECK=false | 15 shots 0 px; only state diff 'items' (W3's two ungated Deck 4 texts, "seven decks": known, fine with the deck on) |
| cadet_test vs 0.63.5 (deck on) | DIFFERENCES, explained: a-d 0 px, e_night onward differ (the rec deck on: the lift's R, crew on rec visits, speech bubbles); state 'items' as above; end state 459 geometries / 179 vs 460 / 180 (BM9's one crew prop: the ship sim runs differently with rec visits). R8: vs cf55b35 ALL IDENTICAL, so RE20's changes move no shot |
| deck_check | DECK CHECK OK |
| machine_check | MACHINE CHECK OK (was FAIL: caches cleared wear, traced faults) |
| career_check | FAILED, only 'busy: "Relied on" before Day 5': **known and accepted** (the user, via lead 20: balance is for the later balance pass; no half-xp constant) |
| day_check 0-8, 14, 21, 28 | all DAY CHECK OK (1, 2, 8 were FAIL on Maeve's rides) |
| events_check | EVENTS CHECK OK (the day 32 '3-galley-5' double is outside its 28 days; known, also on 0.63.4) |
| interactions_check | OK (with RE20's climbing wall case) |
| device_check | OK |
| disc_check | ALL OK |
| mech_check | OK |
| lines_check | PASS (0 errors, 5 warnings, as before) |
| player_check | PLAYER CHECK OK |
| bubble_check, intro_check --week | OK, OK (item D's HUD set) |
| join, food, clothes, smoke, newgame, leave, tiles, path, arc | all OK |
| perf_check vs 0.63.5 | see below |

**perf_check:** draw calls the same or lower in every scene and view, triangles about the same, file 4.94 → 5.13 MB, JS heap 202 → 228 MB (the rec deck's content), load times the same. 'Memory grows across deck round trips' (548 → 548 → 550 geometries) is the same on 0.63.5, so it was there before. The first run, alongside two day checks, flagged 4 scenes' game time a frame (e.g. breakfast 1.31 → 2.94 ms), but other scenes got faster by as much (junior wing 3.75 → 1.32), which looks like load from the other checks. Rerun with one other check running: in progress (added when done).

## For the lead
Green hash: the commit carrying this file on `claude/rec-cand-s1`. Publish it as the NEW artifact "Starship Cadet Rec Deck" (never over the main link).
