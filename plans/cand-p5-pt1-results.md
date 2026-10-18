# Playtest update 1 (0.63.2) check results

Build master 5 (BM5, session_01DbBJ7iK6TrrADyEw7qbCsQ) on claude/p5-cand-pt1; reports to lead 13 (session_015UkCGSS9FyGoBdkePhrKbC). Spec: plans/brief-playtest1.md on claude/lead-pillar1. Base: 0.63.1 = claude/p5-cand-s2 a9fad20. Merge order: C2 claude/works-career, X claude/crew-pt1, P claude/player-p5, O4 claude/arrival-0607b, O5 claude/onboard-pt1, T claude/traditions-pt1, U claude/hud-pt1, A5 claude/deck-pt1 (+ Tern pass 2 484f160), W claude/writer-p5. R2-passed tips only. One line per finished check.

- trial p1 (BM5 scratch 2e4c0ca6) = 0.63.1 + C2 23ef73c + X 2223cb7 + T 1e254bd + U 73b40cb + W 6a00d9c: merges clean (build lines auto), verify 0 missing, bake 9015 lines / 35 traditions, NAMES OK; career, mech, machine, leave, social, newgame OK; smoke 'game failed to start' with 2 lanes (rerun); puzzle_check 205 FAILs 'shown inside the shift' = C2 alone (the check's 480-900 shift window): sent to C2
