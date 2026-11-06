# Handover: build master BM25 (session_01GKuymnYTNkfxgLvtfFRg7w; was BM24 for 0.99.6)

For lead 49 (session_01GKuymjjreuZtZeDMBX79xn, branch claude/lead-49). Read plans/handover-bm24.md, -bm23.md and -bm22.md
(on claude/handover-bm23) first: their steps, tools and gotchas still hold. 0.99.6 is published (integration = main = d7ad4c58).

## State: 0.99.7 merges, all switches off, waiting for JB3's fix
- `claude/staging-0997` from d7ad4c58. Every merge, its clashes and its gate (check_fast, cadet vs 0.99.6 ALL IDENTICAL) are
  in the build-table row "0.99.7 merges (BM25 ...)", items (1)-(17). Pieces in, at their PASS commits: CH1 A 3d07e66 and B
  8436ff6, TP1 c920acb, SC1 77e573f, AV1 15fbf3f, JB3 e96ec5a, TB6 687838e (game 53bf2ce) and B 7b8a061, CR1 3e1b0dc,
  MV1 2e268ba, EV1 dad2b9b and af18afd, GM1 98e612e, CL1 bb26552, SC1's words for TB6 ab0e13e.
- Left: JB3 1bbed58 (35ab083: JB3_FOOD_ON, the galley rule; 1bbed58: machine_check 5v), with RV33. It was the fix for the
  switched-on machine_check FAIL (Day 7 restock; a job without meters), lead 49's call: fix in the game.
- Then: switch-on commit (every switch: `python3 plans/build-master/bm25/switchon.py IN OUT` turns each piece's lines on;
  copy OUT over the game, check the diff is only switch lines), build turn 0.99.7 (setbuild.py), gates on the candidate,
  then plans/round-0997.md's GO line and the GO to R1-R4, R6 (they're set up and waiting) and the lead. I'm R5.
- Trial (scratch branch bm25-trial, not pushed): staging + CL1 + EV1 + JB3 1bbed58, all on: check_fast OK, food 1 7 and
  11 4 OK.

## Gates planned for the switched-on candidate
check_fast; cadet vs 0.99.6 (many differences by design: explain each from the A_/B_ PNGs in the build table); the whole
long checks the pieces touch, not already run by a reviewer on the same file: machine, food, events, bigevents, fridays,
join, tiles, weekend, interactions whole, intro whole, career + cr1_check, player, day 1-7; RV32's fresh_walk (Day 1:
MV1's briefing keep + TP1's nd1 arrow). Two browsers at most; cadet alone at the end.

## Tools (plans/build-master/bm25/)
- switchon.py IN OUT [--off P1,P2]: every 0.99.7 switch on, by piece (CH1 TP1 SC1 AV1 JB3 TB6 GM1 MV1 CR1 EV1 CL1);
  prints how many lines per piece (all must be > 0). CAL997_ON is turned on as `true || URL_FLAGS...`.
- g.sh COMMIT NAME: a worktree, check_fast alone, then cadet vs /tmp/bm24/old-0996.html (make it: git show
  d7ad4c58:starship-cadet.html). cad.sh OLD NEW DIR: cadet alone.
- keepboth2.py FILE: build-table clashes; like keepboth.py, but a row we left untouched takes the builder's newer copy.
- ours_then_theirs.py FILE: clash blocks where both sides only added lines. Read the block first: twice now a plain
  keep-both was wrong (a closing brace dropped between two new functions, MV1 vs AV1; one line changed on each side,
  EV1 vs TP1). Compare each side's lines with d7ad4c58 to see who changed what.
- res_cl1.py, res_cl1_docs.py: CL1's clashes, as done.

## Gotchas found this time
- Bisect with switchon.py --off (one piece off) and with only one piece on: the Day 7 food FAIL came from TB6 alone and
  from EV1 alone (EV997_LIGHT_ON and EV997_SAT_ON each), the galley's knife edge on the Line Sunday.
- FX30's p5retry/fixtap probes need an off copy (round-0996.md). RV32's fresh_walk has no OK line: the pass rule is in
  round-0997.md.

## Open for the user
The builders' defaults in design-doc's Open questions (Pockets, bunk inspection's "not a pass", Spice supper's time, the
board mix, EV1's proposals): switched on by lead 49's overnight rule; the user can change them.
