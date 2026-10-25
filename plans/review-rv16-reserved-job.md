# RV16 review: the reserved-job fix (FX17, claude/fix-reserved-job ba6632b9, game sha256 65da349f...)

Base: claude/integration 5898c190 (0.92.6). Cause (CR1, FX17): 27ad3cba's evMeetClash changed Day 7's plans, so the
machines' wear and the crew's repair jobs moved; on Day 11 both machine-shop making spots were held by crew and the
player's tap at the Lathe found no free spot, so the reserved job stalled.

## Verdict: PASS

- Diff: jobMakeWay(at) in section 15, reached only when both making spots are held: the nearer spot's crew steps aside
  for 20 ship minutes through section 10's existing crewMakeWay (a tile -> until map; no R(), nothing drawn). evMeetClash
  now reads only evMeetsOn and evMeetCast (no venue or lead spots built mid-plan). Small difference from before: every
  cast member's window now starts `early` (default 5) minutes before the meeting, where eventMeetPlan gave slot crew 0
  outside the Line; it can only keep someone out of a clashing tradition a few minutes sooner, and p926_check (the Line
  rule) and bigevents_check pass.
- cadet_test 5898c190 vs ba6632b9 (alone): ALL IDENTICAL.
- player_check: PLAYER CHECK OK (the 3 reserved-job lines fail on 5898c190).
- p926_check: OK. bigevents_check: OK.
- Correction from me: in the sound core re-check I called these 3 FAILs old; they were old only against 5898c190,
  which already had 27ad3cba.
