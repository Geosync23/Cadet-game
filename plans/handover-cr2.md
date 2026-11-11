# Handover: CR2 (career and promotion fixer, lead 51)

**Role:** fixer for lead 51 (session_01GKuymjp49y3M5hgRLecobm); reviewer RV35 (session_01GKuymm7wiTGz6LA46UHffc, PASS; notes plans/review-rv35.md on claude/review-rv35); build master BM28 (session_01GKuymjydss9RxzDw1ftdPf).
**Branch:** claude/p9991-results from main bfbcbdf (0.99.9). Game commit 01cc325 (switch off, game sha256 09d52840...8c62), docs 373c8ee, this note. Published in 0.99.91 (BM28, 2026-11-11; main = claude/integration = cdd9efd, game b321a4ec...95f3).

## The bug and the fix
The user on 0.99.9: "I walk into Calder's office on time and nothing happens" (after a Dev jump). Dev mode's "Day 9: the promotion" jump runs the landing day to 05:00, the game books the 08:15 summons, then section 25's devmodeCareerSet marked every open promotion appointment 'done', so the meeting never played (promoted by Mail at 09:15). Normal play and the other Dev routes were fine. CR1's lead (the excused landing day) was not the cause: it only moves the meeting a workday when you skip past 12:30.
Switch `CR9991_RESULTS_ON` (24p's slot, "CR2 (lead 51 ..."): devmodeCareerSet leaves promoSummons open while `crResultWaiting` (Tier 1, test passed); promoSummonsTick calls `crResultReopen` (a summons Dev mode closed, open again on its day before it ends). Details: DEV_NOTES "The result meeting after a Dev jump".

## How to test
`python3 cr2_check.py BUILD [jump stuck test late]` (about 2 minutes; flips the switch at run time; off it proves the bug is still there, so once the switch is a const or removed, that off case needs updating).

## Gotchas
- Only devmodeCareerSet ever marks an occasion 'done' (RV35); normal play ends them 'kept' or 'missed'.
- A promotion jump landing after 08:45 lets the summons run out as 'missed' (Mail at noon), as in normal play (RV35's note, accepted).
- My first commit trailer briefly carried the lead's session id; amended before pushing.

## Loose ends / open for the user
None.
