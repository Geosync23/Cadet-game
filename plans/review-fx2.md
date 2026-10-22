# Review: FX2's Pillar 5 fixes (claude/p5-fix2)

Reviewer AR2 (session_015pnwa5oK7TDF5gZXNFLLvx), for lead 27, taking over FX2 from PR9. Base: claude/integration 2b4a05db (0.64.15). Builder FX2: session_01JRCSTi6r1qQ51mTgwgJ7es.

How each part is judged (lead 27's brief): its new check part FAILs on 2b4a05db and passes on the tip; honest play in the browser (AR2's bot: it follows only the arrow, taps what the arrow names, uses the board and reads meetings through); cadet_test 2b4a05db -> tip run alone, identical except what's intended; AR1's `arrows_check.py week` (claude/arrows-plan) to see FX2's lines turn green and nothing turn red; clashes with FX1 (claude/p5-fix1) and FX3 (claude/p5-fix3) in sections 15, 15b and 24.

## A. The fire drill (e10d81a4): FIXES NEEDED (one item)

| Test | Result |
| --- | --- |
| mech_check m3d, new "drill by taps" part, on 2b4a05db | FAIL (4 lines: Calendar place, each tap starts nothing, no stop done, no extinguisher), as it should |
| the same on e10d81a4 | MECH CHECK OK |
| cadet_test 2b4a05db -> e10d81a4 | ALL IDENTICAL |
| Honest play, Day 3 (Rounds trained Day 2) | 14:50 toast and "Fire drill, 15:00" on the extinguisher; tap: "Fire drill: about 1 minutes"; arrow "Stand by the hatch"; 10 minutes; "The extinguisher back on its bracket"; "Fire drill: done." at 15:05; 15:15 "Trained: the drill", "All clear", "Two minutes ten. Better."; the arrow gone after the last stop. The bot took a board job straight after. |
| arrows_check week on e10d81a4 | Green now (FAIL on base): Day 3 "m3d" not learned; "stuck from Day 3 14:50 at Fire drill, 15:00"; "Fire drill stayed up over 3 hours"; and "Day 4/5: never clocked in" (they followed from the drill block). Red now, new: "stuck Day 3 15:15 at Repair the galley plant", "stuck Day 4 08:04 and 11:39 at Look over the stage lights (Deck 7)" and its "stayed up" line. Both are old problems the run now reaches because it no longer sticks at the drill: the galley plant one is on base already (09:18); the stage lights' arrow and taps are the same on base and tip (probe: jobHere at 7-aud-lights-svc works on both), and FX2 didn't touch the machine arrow or taps. Not FX2's. |
| Trial merge FX2 + FX3 b063f86 + FX1 1433e5f | Conflict only in plans/build-table.md. Played Day 3 on the merge: FX3's Calder briefing shows at 14:50 (before the drill, as it should), then FX2's arrows take you through; all done at 15:05. No clash in setGoal/clearGoal: drillGoal only touches a goal tagged with the drill's id. |

**Fix needed (A1).** The drill job is posted and claimed for you at the 14:00 hour (`post(h)` with h = 14; `found` = 14:50), and `ixSides()` offers it at once. So from 14:00 to 14:50, before Calder's call, a tap on the extinguisher (on the Works bay wall by the board, the sort of thing players tap to read) starts the drill silently. Reproduced at 14:13: "Fire drill: about 1 minutes", the extinguisher in your hand, `j.reached` = -45 (a "fast" muster), and at 14:50 the toast and arrow point at a stop already done. Suggested: `ixSides()` only offers a side job once it's announced (`j.found <= shipNow()`, or `j.told` for the drill); before that the tap shows the extinguisher's description as before. One line in the m3d part (a tap at 14:20 starts nothing) holds it.

**Notes (not blocking):** the step toasts are titled "Your job" and say "about 1 minutes" (old wording in 15b's chore path); Calder's word "Two minutes ten" is a fixed line, not the real time (old).

## B. The scanner: not received yet

## C. Wording, the galley plant's calibrate, a dropped part left in hand: not received yet
