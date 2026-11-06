# Handover: build master BM25 (session_01GKuymnYTNkfxgLvtfFRg7w; was BM24 for 0.99.6)

For lead 49 (session_01GKuymjjreuZtZeDMBX79xn, branch claude/lead-49). Read plans/handover-bm24.md, -bm23.md and -bm22.md
(on claude/handover-bm23) first: their steps, tools and gotchas still hold. 0.99.6 is published (integration = main = d7ad4c58).

## State: 0.99.7 built, GO sent ~13:00 UTC; BM26 (session_01GKuymkyzjd6auLTCEZK5CN) takes over R5 and the record
- `claude/staging-0997`: every piece merged (build-table row "0.99.7 merges", items 1-17), JB3 1bbed58 at 4e2f5fb,
  switch-on 3a0dbe6 (21 switch lines), build turn 363107d, docs to 7fd8f6b (GO line in round-0997.md). Candidate game
  sha256 b14421f82e04602cd608505756ddb8fb05bea4571af813d8e345424ebcd1cf7d. Lead verified. GO sent to R1-R4, R6.
- My early gates on that exact file (/tmp/bm24/wt-t2 in my container, summary /tmp/bm24/t2/summary.md): check_fast OK,
  machine OK, events OK; interactions whole, bigevents, join, tiles, weekend, fridays, cr1, career, player, day 1-7,
  fresh_walk were running at handover: results are in the 0.99.7 build-table row once in.
- R5 left (script /tmp/bm24/r5b.sh, also in this note): machine (2nd), mech, disc, clothes, promo_beats, food 1 7 and
  11 4, stories 36, day 3, 12, 13, 17, 18, 19, 27, p5retry_break (off copy: P5_RETRY_ON and FIXTAP_ON false), then cadet vs
  0.99.6 alone: list every difference in the round record (soles, hair, seat poses and seats, sofas, tracker/tips, film...).

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

## Early gate results on b14421f8 (final, 2026-11-06 ~15:00 UTC; sent to BM26 and lead 49)
OK: check_fast, machine, events, bigevents, join, tiles, fridays, cr1, career, player, day_check 1-7, fresh_walk Days 0-3
(0 errors, 0 stuck). NEW FAILs: weekend_check (still expects the Saturday run, cut by CL1's CAL997_ON: check-side, likely);
interactions_check whole: (a) the crew store not on the week-1 Schedule (CL1 note 15: check-side, likely), (b) "the Orange
tree tapped off the pin is the garden, not the vent (None)": unplaced, needs a bisect. BM26 owns the round from here.
