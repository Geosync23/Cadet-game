# Handover: FX30 (fixer, lead 39 then lead 40), 2026-10-26

## Done
- claude/week-guide-fix fa6b7de0 (from claude/integration d9c7e5f0, test only, game unchanged): arrows_check week guide
  stalls (Theo Day 6 20:10, toilet Day 7 18:20) were a check gap: the follower's tap at the pin opened a chat card it
  never answered. Fix in FOLLOW: in a line (QUEUE_YOU) is an answer; a chat card gets "Sit with them" for the arrow's
  "X wants a word", else closed. Bisect: e31aaea2 OK, 62034736 (INSPECT_ON) FAIL (the inspection moves the crew's day).
  All checks OK (build-table row "week-guide-fix"). With BM18 to merge; CR1 reruns the week guide.

## Not started: the stale team-job arrow (RV20's S2, claude/review-rv20 394d7d51, plans/review-rv20.md)
Seen: invited to a team job ("Scrubber fan change ... Your turn: hold it steady" 09:34), then "Emeka started without
you" 09:45; the game arrow stays on "Tap the lift: Deck 4 · hold it steady" for hours.

Suspected code (section 24h, team jobs; not yet run to confirm):
- teamNext (~line 57016): on your turn it calls setGoal({ deck, room, label: TEAM_PART[s.part] }), a plain IX_GOAL with
  no done() test, so only something that clears IX_GOAL removes it.
- teamLate (~line 57032, "started without you"): hands your steps to the lead (s.who = j.lead), sets j.late, toasts
  team.late, but never clears that goal. teamEnd doesn't either. "Tap the lift: Deck 4 · " is just the lift prefix the
  arrow adds when you're on another deck.
- Likely fix (small, section 24h, owner per plans/owners.md): in teamLate (and teamEnd) clear the goal if it is this
  job's: e.g. `if (IX_GOAL && IX_GOAL.label === TEAM_PART[<a part of j.seq>]) clearGoal();` or tag the goal in
  teamNext (setGoal({ ..., team: j.id })) and clear when IX_GOAL.team === j.id. Check section 15's goalNow/arrow queue
  doesn't also keep it (with GUIDE_ON the IX_GOAL may be wrapped as a queue entry).

Repro idea (not run): on 0.93.2, a Dev save where you're invited to a team job; let your turn come (the "hold it
steady" arrow appears), go to another deck and stay past 15 minutes; after "started without you" read goalNow() and
IX_GOAL: the arrow should be gone. A check for it fits interactions_check or mech_check's m8 part.

## Gotchas
- Background runs started with `&` inside a Bash call can be cut off when that call ends (EPIPE); use the tool's
  run_in_background with a long timeout. Don't `pkill -f` a pattern that appears in your own command line.
- interactions_check took ~30 min under load (8 min alone).
