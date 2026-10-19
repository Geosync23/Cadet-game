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

## Loose ends at handover
(filled at handover time)
