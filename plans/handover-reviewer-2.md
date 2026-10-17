# Handover: Adversarial reviewer 2 (Pillar 4)

**Now held by reviewer 2b** (from 2026-10-17 ~08:50). Round 1 (5ac9d26): crowd-render d45d019 PASS; decks 3e1f4f9 PASS (closes items 1 and the trestle half of 2; end chairs LOW); ship-events 3d06bcb PASS (closes item 3); device e5d7227 PASS WITH FIXES (two HUD MUST-FIX). Round 2: crowd-render 287a6b0 (0.27.27) PASS; dialogue 0b504ba (0.43.26) PASS WITH FIXES (MUST: chatter pre-empts the spread-out overheard scan, 8 vs 7 conversations; LOW: cue memo keyed on length); device 9180271 (0.35.35) PASS. Already passed before, per the lead's re-asks: dialogue 46e948b, tiles 99609d3. Round 3: device 812abfa (0.35.36) PASS (HUD fixed); content 5e2605e..fd3db63 PASS (0.48.50 needs dialogue 0.43.27+, else lines_check 19 errors); dialogue c084a1a (0.43.27) PASS WITH FIXES (MUST: pair:mentor either-way vs lines assuming B mentors A); galley 2bfd042 (0.29.33) PASS. Round 4: device 15bc0fa (0.35.37-38) PASS (missed-then-kept played on a merge with sim 236810f + social 0154e8d: stays missed, no points; lead to decide whether section 18 should still play/keep the occasion; device_check's 'as it starts, once' fails on that merge only because Late piano shares the window); crowd-render f2a682d (0.27.28) PASS (GPU buffer mirror via wrapped gl.bufferData/bufferSubData vs chunk arrays: 0 mismatches; no-pv/pi control: 120). Round 5: content 92866aa (0.48.51) PASS WITH FIXES (voice cards/briefs still say ladder & skipped breakfast; game text clean); dialogue 754ddbd (0.43.28) fixes 0.43.26 (same 8 overheard as 0.43.25); device c89f00f/24f1920 (0.35.39) PASS; ship-events 2ffff6f (0.34.50, New game reset) PASS on 0.60.3+device merge. Lead ruling: 'late but you came' is fine (occasion kept + keepsake, device stays missed). 0.60.3 alone fails device_check 'From home, Play' (pre-existing). Round 6: galley 7282327 (0.29.34) PASS (Sunday wait 6->0; food_check galleyJoin/galleyTurn FAILs with sim e1bb1e6 for 0.29.33 and 0.29.34 alike: sim 0.26.35+ vs the check); dialogue ff2c3d6 (0.43.29) PASS (all closed); content fe380dd PASS (needs 0.43.29: pair:mentee); crowd-render 870ee00 (0.27.29 heap findPath) PASS (path_check on branch and on a sim+decks+events merge with another seed, incl. a Sunday with the trestle). Round 7: galley 7464b97 (0.29.35) + food_check a0e5b2f PASS; crowd-render 975e0e5 (0.27.30 kept bodies: packs re-derived from spec match on days 1-300) PASS. Round 8: social-stories 788b4af (device_check Gran message) PASS; crowd-render f0898c3 (0.27.31) PASS. Asked to carry the device_check fix onto claude/device: declined (reviewers write only to claude/reviews-2); the lead ruled build master 2 carries it in the combine. Round 9: crowd-render abe6d2b (0.27.32) PASS. Gotcha: when the container is slow, cadet_test's 30 s page.goto times out; use a scratch copy with page.set_default_navigation_timeout(240000). Don't pkill chrome (it killed my shell). Round 10: galley 7b81f4a (0.29.36) PASS; crowd-render 73b8998 (0.27.33, stand-ins over frames, perf engineer 3 = session_01S8FWAPFnpaAAUN1wpDQbbo) PASS. Queue empty. Dialogue tests need claude/content baked in (git checkout origin/claude/content -- content; python3 content_gen.py the.html). cadet_test can flake under load: the soft heads-up card closes on a real-time timer. Don't name a probe variable HOOK (cadet_test uses it). Probes this round (scratchpad): a frozen-matrix drift check over a ship day per deck; long-table seat occupancy (no trestle sitter while a room seat is free for the whole stay); HUD box overlaps at 13 viewports with all 130 room names and every weekday's clock.

**Written:** 2026-10-17 ~06:40 UTC; final refresh ~08:40 UTC, when reviewer 2 stood down (the lead's call, memory getting full). **Refresh this right before an actual handover** (latest hashes, anything in flight).
**Branch:** `claude/reviews-2` (review notes only, under `plans/reviews/`). I write NO game code.
**Report to:** the lead, session_01KPJMYjXAPkNUcrQ8VRkhLE (since ~04:35; earlier leads 01PJtmxW... and 01PxXKwc...),
and for anything going into a combined build, also build master 2, session_01F8ph7FKqViF3heRn94YgBr.
Chain of command: only the lead talks to the user.

## My seats and their state (last verdicts)
| Seat | Branch | Engineer (session) | Last passed | Open from me |
| --- | --- | --- | --- | --- |
| Dialogue (section 22, content_gen, lines_check) | claude/dialogue | dialogue eng 2, 01S26bs4oMahyGJkuVaCKQGT | 46e948b (0.43.25) | none |
| Traditions (section 18, .trad, events_check) | claude/ship-events | traditions eng 2, 01WEEoe5DyRegEqVMZgKRHWB | 4631a97 (0.34.48, PASS; extras-as-overflow design note) | meal-tradition turnout waits on the sim's `meal` work (not this seat's) |
| Device (section 19) | claude/device | device eng 3, 01SskqNx45iEGyQq2W9Fjg5Y | ee3fcdd (0.35.32) | none |
| Decks (DECKS, DECK_DRESS) | claude/decks-p3 | deck architect 2, 01ToE6RJFCw9deB3HcJRLKxS | a71ac47 (0.38.20): ternClear still ignores DECK_CREW (one-line fix asked); trestle walk-through LOW | Tern plan sketch 8e8894b: PASS WITH FIXES (to the plan; reviews/decks-p3-8e8894b-tern-plan.md); check the build against it |
| Performance (sections 4c/5, lead-assigned) | claude/crowd-render | lead | cfbfd76 (0.27.25) | none; context-restore note in reviews/crowd-render-cfbfd76.md |
| Tiles (section 23) | claude/tiles | Tiles eng (idle; handover plans/handover-tiles.md) | 99609d3 (0.46.6) | none |
| Content (content/ only, for combines) | claude/content | build master 2 asks per range | a3f151a..5d4b810 (0.48.47, PASS WITH FIXES) | Tomas's week-1 beats assume Fri/Sat off (game: Mon/Tue); facts.md days-off stale for 52/74 crew |
Combined builds: 0.60.2 released (142b503); build master 2 is combining 0.60.3 on claude/cand-0603.

## Known issues outside my seats (reported, for others)
- events_check FAIL `231 dayReport double: 3-store-1 esposito-yara/ishikawa-orla@14:30` is pre-existing (it reproduces on
  0.60.0): the store till's 14:30 hand-over (sim/store owner).
- Meal traditions: turnout now 32+ on Sundays and 45 at the harvest supper (with decks a71ac47 + traditions 4631a97).

## Rules I enforce (and found broken before)
- **Duplicate top-level consts across branches** merge silently and break the parse (TRADITIONS, TILES): trial-merge
  and `node --check` the script whenever two seats add generated blocks or kit names.
- **Generated blocks:** content_gen.py must be re-run after merging dialogue (its branch bakes only Sowing).
- **No romance with the player, ever:** lines_check's BANNED list plus the head writer's read. Couple words are allowed
  only in overheard pair:couple/bond:couple lines with no player reference; calls home exempt only plain "love you";
  home contacts limited to mum/gran/jo/sam. Probe new kinds with lines like "in love with the new hand", "my love",
  "Are you seeing anyone, {me}?", "Rumour is {me} and Pell are dating".
- Determinism: plans must be pure (affinityPlan, not affinity); crew randomness via schedU in the seat's key range.
- Rewards: daily caps per person (chat is once a day; Tiles copies it).

## How I test (all in my scratchpad; recreate as needed)
- three r128: `mkdir -p $W/three && cd $W/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz`; run checks with
  `CADET_WORK=$W CADET_CHROME=/opt/pw-browsers/chromium-1194/chrome-linux/chrome python3 events_check.py starship-cadet.html [DAYS]`
  (use an absolute CADET_WORK; 7 days fails hull-lights by design, so use the default 28 for verdicts).
- Probes: import cadet_test as a module with sys.argv set to [x, path, path] and use Game(pw, path).ev(js).
- Trial merges in a worktree; resolve the build-label conflicts by keeping HEAD; then `node --check` the largest <script>.
- lines_check probes: drop small files into content/banks|overheard|arcs|home of a dialogue worktree, run content_gen
  into a copy of the html, then lines_check (ignore its "out of date" line).
- My independent Tiles simulator: plans/reviews/tiles-5aa442c-sim.py.

## Open items (with hashes), final state
| # | What | Where | Last seen | Waiting for |
| --- | --- | --- | --- | --- |
| 1 | `ternClear()` checks only `walkers`; a DECK_CREW escort on the ramp/well [5,8]/[5,9..10] isn't seen, so `ternRamp(false)`'s refusal (0.38.19) still closes on crew | claude/decks-p3 | a71ac47 (0.38.20) | the deck architect's one-liner; verify in a browser by putting `DECK_CREW[0]` on [5,8] and calling `ternClear()` (must be false) |
| 2 | The trestle and end chairs (DECK_DRESS longTables/harvestTables) don't block tiles: crew walk through them on the promenade | claude/decks-p3 | a71ac47 | the tile-blocking fix (incoming) |
| 3 | The long-table extras fill alongside the mess seats (Sunday day 7: 9 of 32 on extras) | claude/ship-events 4631a97 + decks a71ac47 | 4631a97 | the traditions + sim overflow flag (incoming): check the room fills first and the harvest supper still uses all 13 |
| 4 | Tomas's Saturday 11:45 garden beat says "my lunch break", but no lunch is planned, so he's on watch on Deck 2 unless onboarding brings him | claude/content 5e2605e | 5e2605e (0.48.48) | the onboarding hook (an appointment or crewHold) |
| 5 | Night-shift honorees miss the rotation suppers (day 244 Lars Achterberg, day 250 Jem Castellano) | ship-events events_check 9d | 2951e5b | sim 4's section 14 0.26.31; recheck 9d after the combine |
| 6 | Tiles crewHold: code reviewed only (crewHold is on claude/sim-engineer bfcd864) | claude/tiles 99609d3 | 99609d3 | first combined build: start a game, walk off, the opponent rejoins their plan |
| 7 | Graphics context loss: the picture is wrong after a restore in both builds (no restore handling); the shadow stand-ins free their CPU copy | claude/crowd-render cfbfd76 | cfbfd76 (0.27.25) | if restore handling is added, it must call `shadowStandIns()` again |
| 8 | Combine dependencies: dialogue 46e948b + social 0811adc + roster caedef2 + content 5e2605e together ({kin}/{lost}/{hobbyNoun}); decks a570274+ with sim 4 and onboarding moving SHIP_START_ARRIVAL / INTRO_START to [5,7] | build master 2 | - | 0.60.4 |

Incoming per the lead (not yet reviewed): decks ternClear fix + trestle blocking; perf 0.27.26 and 0.27.27 (crowd posing; check
pixel-identical shots, the shadow stand-ins and noMerge movers); traditions + sim long-table overflow flag; the device's HUD clock fix.

## Loose ends / next
- DONE: the theme fill-in fix ({kin}/{lost}/{hobbyNoun}): dialogue 46e948b, roster d53cf40..caedef2, content 5e2605e all passed.
- Content reviews come from build master 2 as ranges of content/ only (last passed: a3f151a..5e2605e). Check tone, romance, names
  not aboard, serious lines in week 1, self-naming, lines_check PASS, and facts.md against the roster (days off, work decks).
- Re-check the meal-tradition turnout once the sim's `meal` hook lands.

## Useful scripts I wrote (scratchpad, gone with this session; easy to rewrite)
- Days-off check: parse facts.md's `| `id` | name | role | shift | days off |` table and compare it with ROSTER rota.offDays
  (`weekday` 0 = Monday).
- VOICE/LINES equality: eval both blocks in node and compare JSON.stringify (catches key order).
- Rotation/long-table seat counts: planDay(p, d) segments tagged `ev-<id>` and their placeId.
