# Handover: build master 7 (BM7, session_01QbuzvT3TwzMwSWRmakzX8Z)

**Role:** combine the seats' reviewed tips into one candidate build, run the checks, send failures back with evidence, give the lead the green hash. **Branch:** `claude/p5-cand-s4` (BM7's only push branch). **Build:** 0.63.4 (Pillar 5 Step 4, side jobs, + playtest update 2 pieces if passed in time). **Lead:** lead 17, session_016bN7x175WBwBL7S9xc2Lpb. **Reviewer:** R6, session_01CPyuA1o5jgxwQtv7huZTNg (R4, R5 retired). **Second check runner:** CR2, session_018xWmWkrtNWudZUgXygkW1u (notes to `claude/p5-cand-s4-checks`). Log of every trial and result: `plans/cand-0634-results.md` (read its last 30 lines first).

## Base and seats
- Base: 0.63.3 released = `claude/p5-cand-pt1` 2bc08d5 (game = 7a6e137).
- Merge order (brief p5s4 + lead 16): 24 core (E1→E6, claude/mech-rounds) → mechanics (E2→E5 claude/mech-incidents; E3→E4 claude/mech-diagnose) → cases → places → X (X2, claude/crew-pt1) → U (U→U2, claude/hud-pt1 / claude/hud-pt2) → W2 (claude/writer-p5, retired; final 0e8571a).
- Seats now: E4 session_01PtXCwVBprdkJ6AcQisEyJq, E5 session_01QsZymCraDjLzVDooLvigNk, E6 session_018cZuXpb4XdFs47zXoPcF8B, X2 session_016jw3fP3pGztfciWgr6hg9A, U2 session_012TFwzt5eZoNZKrXrXTzN2w. Retired: E1, E2, E3, W2, U.

## Container setup (fresh session)
`pip install playwright`; `mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz`; `export CADET_CHROME=/opt/pw-browsers/chromium`. Tools: `ln -sfn <scratchpad>/cw /tmp/cw; cp -r plans/build-master /tmp/cw/bm; cp plans/build-master/union24.py /tmp/cw/union.py`, then recreate /tmp/cw/mk.sh, teach.py, q3.sh (copies in plans/build-master/bm7/).

## Recipe
- `mk.sh WT OUT tip...` merges tips onto 2bc08d5 in worktree WT: build lines auto (resolve.py), mech_check conflicts keep-both (unionall.py), the teach-loop combine (teach.py), **stops if any tip did not merge** (a quick loop without that check once skipped E6 silently), sets 0.63.4, bakes, NAMES, node --check, verify_merge.
- `q3.sh HTML TAG check...` (WT=worktree, OLD=base copy, TMO for player 2700) runs checks one after another, one line each in /tmp/cw/logs/summary.txt, **each run with its own CADET_WORK** (R6's find: checks copy the build to $CADET_WORK/test/; parallel runs with the default share fixed names `_career_save`, `_mech_save`, `_save_budget/_save_check` and can test the other build). At most 2 browser checks at once.
- cadet_test base copy: `git show 2bc08d5:starship-cadet.html > c0.html; setbuild.py c0.html 0.63.4`.

## Hand merges seen (all expected again)
1. mech_check.py: every seat adds parts after `part_m9` and calls in the main loop after the rows loop: keep both, in merge order. Result must have the EXTRA loop exactly ONCE (with E5's tparts condition) and then E4's `part_t24` call; all of part_side, part_mrun/haul2/stock, part_round23, EXTRA, part_t24 present; `python3 -c "import ast..."` parses.
2. Game file section 15 teach loop: 24 core's `tipShow(id, bedText(text))` vs U's function texts → `let tx = text; if (typeof text === 'function') {...}` then `if (tipShow(id, bedText(tx)))` (U2 writes `tx && bedText(tx)`: same).
3. verify_merge "explained" set: the 3 old versions of that line; 6 E1 0.45.8 lines E3/E4 carry that E1 0.45.10/11 rewrote (m11 row, side save line, two toolWear lines, two side-XP lines); 2 'still here' under E6 f36d81e (moved, not deleted).

## Known results (details in the log)
- E1×E2 key-order career FAIL → fixed by E1 fb499eb. X2 ec0cbc3 machine 'hauling misplaced part' FAIL → fixed in X2 693e4f4 (checked alone). X2's crew wake changes every cadet shot (all X2's; t11 = base+X2 alone, same px).
- Trial t14 (E6 f36d81e, E5 2c513e6, E4 2b5979a, U 0335523, W2 0e8571a): see log.

## STATE AT HANDOVER (~08:23 UTC) — BM8 takes over
- **Lead 18** (session_01CBur9nrJ411pFkHopF96RL) decided: 0.63.4 = the no-X2 candidate. X2's crew pieces (0.71.3-0.71.6) go to 0.63.5 (BM8, claude/p5-cand-s5); R6 passed X2 693e4f4, 6c26c72 still in review; in the combine 6c26c72 FAILs mech_check m12 + tparts (X2: tparts is first-run state the TPARTS reset doesn't clear: a warm-up run in the check; m12 not yet placed) and ixtap-3-lift-1 in interactions (BM8 placed it on X2 alone).
- **Final candidate = `claude/p5-cand-s4` c336170** = 92d40d5 (game file) + U2 06a5e99 (interactions_check.py only, R6 PASS: the round-guide stub now rebinds roundTrainStep). Game file identical to 92d40d5.
- **Results on 92d40d5's game:** OK: mech, career, machine, lines (0 errors, 2 warnings), cadet ALL IDENTICAL vs 0.63.3 (0 px), puzzle, social, day0; CR2 14/14 OK (smoke, newgame, events, device, food, clothes, arc, deck, path, tiles, disc, bubble, join, leave; claude/p5-cand-s4-checks 26be4a3). interactions FAILed only the round-guide tip lines = the check bug fixed by 06a5e99.
- **Still to run on c336170 (BM8, in your own container, own CADET_WORK each):** interactions (with 06a5e99's check; U2 is also running it and will report), day 1-8, intro --week (alone), player (TMO 2700). BM7's container was running day1+ and player at handover but nobody will log them: rerun.
- **When green:** finish the DEV_NOTES 0.63.4 row (it says "(in progress)": add the check list above, the hand merges are already in it, note X2 left out → 0.63.5, U2's check fix), commit + push on claude/p5-cand-s4, send lead 18 the hash + summary. If BM8 can't push to claude/p5-cand-s4, ask lead 18.
- **Fallback if the game itself fails something:** tf3 = the same with U 0335523 instead of U2 0f34cfb (t14 green); rebuild with mk.sh (tips 5bd6f97 2c513e6 b0cb86c 0335523 0e8571a) + the roofTalk guard fix.

## Loose ends at handover (~08:05 UTC)
- **Lead is now lead 18** (session_01CBur9nrJ411pFkHopF96RL). E1, E2, E3, E4, E5, E6, W2, U retired/archived; X2 and U2 active.
- **0.63.4 candidate WITHOUT X2 = `claude/p5-cand-s4` 92d40d5** (E6 5bd6f97, E5 2c513e6, E4 b0cb86c + the roofTalk guard merge fix, U2 0f34cfb (contains U 0335523), W2 0e8571a). Same game file as /tmp/cw/tf2.html. DEV_NOTES 0.63.4 row says "(in progress)": finish it with the results; the CADET_WORK Testing line is in.
- **Full round running on 92d40d5:** CR2 (session_018xWmWkrtNWudZUgXygkW1u): events, device, clothes, food, deck, tiles, bubble, join, smoke, newgame, leave, arc, path, disc. Mine: tags tf2 (mech, career, machine, lines, cadet), tf2i (interactions), tfA (puzzle, social, day 0-8, intro --week), tfB (player, TMO 2700) in /tmp/cw/logs/summary.txt. If the container restarted, rerun what's missing from the summary (q3.sh, WT = a worktree at 92d40d5).
- **X2 timebox ~08:55** (lead's call): X2 6c26c72 (0.71.6) breaks mech_check m12 (night crew / logbook) and tparts (team parts) in the combine (OK without X2; X2 alone base+X2 machine OK). X2 is bisecting on 92d40d5 for 0.71.7. Green by 08:55 → merge X2's tip on 92d40d5 and re-run cadet (vs base + X2 alone: X2's crew wake changes every shot), mech, interactions, day 0-8, intro, deck, food, events, machine; else 92d40d5 is 0.63.4 and X2's 0.71.3-0.71.x go to 0.63.5 (BM8).
- **Open: t15 interactions FAIL** (with X2 + U2): 'ixtap-3-lift-1: a tap at the stop (lamp, Deck 3) starts the work' and the take/go/look tip-arrow lines all empty. t14 (U 0335523, no X2) was OK. tf2i (no X2, with U2) answers whether it's U2's or X2's. U2's 0f34cfb has no R6 verdict yet that BM7 saw: ask R6.
- **Send lead 18 the final hash + summary** when the round is green.
