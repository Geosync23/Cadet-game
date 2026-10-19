# Handover: build master 6 (BM6, session_01F8k6hqdBRoxDJMzqAuiHqR)

**Role:** combine the seats' reviewed tips into one candidate build, run the full check set, send back failures with evidence, and give the lead the green hash. **Branch:** `claude/p5-cand-pt1` (this session's only push branch; the lead copies green hashes to `claude/p5-cand-s3` / `claude/ship-integration`). **Lead:** lead 16, session_01UMyfd16GqSdgNyz5PE8qSv. **Reviewer:** R4, session_01UGQxniXCxT5TLEE4tgRLfJ (R3 stopped). Take only tips the reviewer has passed.

## Builds done
- **0.63.2** (playtest update 1) = `claude/p5-cand-pt1` 86dcda1, green; log plans/cand-p5-pt1-results.md; DEV_NOTES row.
- **0.63.3** (Pillar 5 Step 3) on 0.63.2r (ship-integration 898d58d) = `claude/p5-cand-pt1` 7a6e137 (game file; later commits only add notes). In merge order: S2 `claude/ship-systems` 0d0aa59, C2 `claude/works-career` f553607, M2 `claude/mech-incidents` b3e5cf9, M3 `claude/mech-diagnose` 42c76cc, H2 `claude/mech-cases` 935b1d9, DA5 `claude/deck-p5s3` 25dbfce, X `claude/crew-pt1` 3a494c8, U `claude/hud-pt1` 1d602ff, W2 `claude/writer-p5` a21487e. Log: plans/cand-p5-s3-results.md (every trial, every fail and whose it was).

## Recipe (plans/build-master/)
- Container setup (fresh each session): `pip install playwright`; three.js r128: `mkdir -p /tmp/cadet-work/three && cd /tmp/cadet-work/three && npm pack three@0.128.0 && tar xzf three-0.128.0.tgz`; `export CADET_CHROME=/opt/pw-browsers/chromium`. BM6 kept tools in the scratchpad with `/tmp/cw` symlinked to it: `cp -r plans/build-master /tmp/cw/bm`, `cp plans/build-master/union24.py /tmp/cw/union.py`, mg.sh = mergep5.sh with the build number edited, q2.sh = checks2.sh (takes `WT=<worktree>` and `OLD=<base html>`), logs in /tmp/cw/logs, one line per check in /tmp/cw/logs/summary.txt (watch it with Monitor `tail -n0 -f`).
- Worktrees: one per trial (`git worktree add /tmp/cw/wtN <base>`), never two sharing a branch name; checks run from the worktree's own scripts (the merged versions).
- Merge: tips in the brief's order; build-line and DEV_NOTES conflicts via `resolve.py starship-cadet.html <build>` and `resolve.py DEV_NOTES.md <build> --union`; anything else STOP and look. **Always run `setbuild.py starship-cadet.html <build>` before baking**: with no conflict a seat's own build number wins, and the HUD label's width then shifts the top button row in cadet_test (BM6 lost time to this). Then `content_gen.py starship-cadet.html` (and `--check`), `name_check.py` (duplicate top-level names), `node --check` on the script, `verify_merge.py <base> HEAD starship-cadet.html <tips…>`: explain every MISSING/STILL-HERE (usually a later tip's rewrite, or a seat that removed and restored a block).
- cadet_test: compare against a copy of the base with the same build label (sed the header line and GAME_BUILD) so only real changes show; place any difference by building partials (base + one tip, or the set minus one) and comparing those.
- Placing a fail: rerun the check on base + the suspect tip alone, then add tips one at a time. Send the seat the exact FAIL lines, the builds tried and which passed. Most Step 3 fails were two seats' pieces meeting (check wording vs writer's text, two locks on the same doors, a stage reading a row another seat moved into core), not either seat alone.

## Hand-merge spots seen in Step 3 (expect them again in Step 4)
- Section 24 blocks appended before `// 6. CAMERA` by several seats (C2's 24p, M2's 24h, earlier M1/M2 24a-f): keep both, in merge order (`unionall.py <tip> <file>` keeps ours then theirs).
- mech_check.py: new `part_mX` blocks and `PARTS[...]` lines side by side (keep both); the frame's `doJob` line (M2's teamDo/doJob replaces the plain one; C2/H2's two `W.tier`/`needs` lines stay above it).
- `jobStopsBase`: S2's `traceHidden … traceStops` line first, then H2's `machineById((caseAt…) || j.machine)` line (drop the plain machineById line). `jobCard`: H2's caseCard line before the machine line, S2's traceHidden after it (each seat's own order).
- edgeBlocks / the door loop (section 4/11): DA5's YOU_LOCKS is the one lock; C2 supplies `bridgeBarred`.

## Check split with a second runner (lead starts it; ~45 min instead of ~1.5 h)
- Mine: cadet_test vs base, career, mech, machine, puzzle, social, lines, player (TMO 2700, ~20-30 min), day_check 0-8, then intro_check --week ALONE (always pass --week: with no flag it runs every part and hits 30 min).
- Runner: interactions, events, device, clothes, food, deck, tiles, bubble, join, smoke + newgame (plans/build-master/*_check.py with cadet_test.py symlinked next to them), leave, arc, path, disc. It needs the hash, the container setup above, at most 2 at a time, one line per check back to you.
- At most 2 browser checks at once on one box (a third gives "game failed to start"). Never pgrep -f/pkill by pattern (BM5: it killed its own shell); find PIDs with `ps -eo pid,args` and kill by number.

## Loose ends at handover
- 0.63.3 final round: see the last lines of plans/cand-p5-s3-results.md for what finished; DEV_NOTES 0.63.3 row added with the green hash.
- Step 4 (E1-E3 start on 7a6e137) is for the next build master; BM6 did no Step 4 merges.
