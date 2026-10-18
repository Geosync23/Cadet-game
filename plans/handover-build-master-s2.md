# Handover: build master 5 (BM5, session_01DbBJ7iK6TrrADyEw7qbCsQ), Pillar 5 Step 2 and playtest 1

**Lead:** lead 13 session_015UkCGSS9FyGoBdkePhrKbC (took over from lead 12 ~15:52). Report: final hashes, blockers, design calls only. **Reviewer:** R2 session_01DZoxp9pxhp63Wye1Kr2MsZ (plans/reviews-p5-step2.md on claude/reviews-p5-step2, "Passing tips" at the top). Take only R2-passed tips.

## Done
- **0.63.0** (Step 1) = claude/p5-cand **093bdd6**: p5-join 6e730b1 + A 6cc826b + W 0d179ac + P 3373828 (0.28.73) + test-only fixes (S 0e18118 social, P f00ac1e/d6f321d player). Shipped with one player_check FAIL written up (fixed later by P ad9ff57). Log: plans/cand-p5-results.md.
- **0.63.1** (Step 2) = claude/p5-cand-s2 **a9fad20**: 0.63.0 + S 0e18118, P f2156f1, C 8cc07a5, O4 96649fe, M1 ec9b498, M2 c9b211a, W ac60c8d. All green incl. day_check 0-8 and intro_check --week. Log: plans/cand-p5-s2-results.md; DEV_NOTES 0.63.1 row.

## Next: 0.63.2 (playtest update 1) on claude/p5-cand-pt1
- Spec: plans/brief-playtest1.md on claude/lead-pillar1. Base 0.63.1 a9fad20. Merge order: C2 (claude/works-career), X (claude/crew-pt1), P (claude/player-p5), O4 (claude/arrival-0607b), O5 (claude/onboard-pt1), T (claude/traditions-pt1), U (claude/hud-pt1), A5 (claude/deck-pt1, + Tern pass 2 484f160), W (claude/writer-p5, text; run content_gen). Seats send hashes directly; R2 must pass each.
- Known at handover: C2 fd26e15 (0.44.14) not passing alone (needs 0.44.15); W's tip moves often (last seen a6593a8/ff81441, all text, R2 PASS). Do NOT take claude/ship-systems head (paused Step 3 piece e82abed); S stays 0e18118. Do NOT take claude/mech-incidents 42e83cf (merges S); M2 code = c9b211a.
- Full set: cadet_test vs 0.63.1, career, mech, machine, puzzle, social, smoke, newgame, food, deck, leave, device, lines, tiles, events, clothes, arc, interactions, path, player, day_check 0-8 (09:00 shift), intro_check --week ALONE. Build number 0.63.2 (resolve.py sets build lines), DEV_NOTES row.

## Tools (copies in plans/build-master/)
- `mergep5.sh WT BASE OUT.html TIP...` (= /tmp/cw/mg.sh): merges tips onto BASE in worktree WT, build lines via resolve.py (edit the 0.63.1 inside it to the new build number), `union24.py` for the M1 24a / M2 24e block and mech_check PARTS, STOPs on any other conflict, bakes to OUT. Then run verify_merge.py and name_check by hand (see results lines).
- `checks.sh HTML TAG check...` (= /tmp/cw/q.sh): sequential checks from the worktree, one log each in /tmp/cw/logs, one line each in /tmp/cw/logs/summary.txt; `dayN` = day_check N; `cadet` = cadet_test vs $OLD; TMO sets the timeout. Run at most 2 lanes at once (a third gives "game failed to start"); player_check needs TMO=2700 (~33 min); intro_check --week alone (~200 s on a quiet box).
- smoke/newgame checks live in plans/build-master/ and exec cadet_test.py from their own folder: symlink cadet_test.py next to them.
- Gotchas: a check copied under another name breaks its `__file__.replace('x_check.py', 'cadet_test.py')`; never pgrep -f/pkill by pattern (it matched and killed my shell); `git add -A` would pick up cadet_test screenshots in the worktree, add files by name; a chained `&&` merge stops silently on a build-line conflict (use the script).
