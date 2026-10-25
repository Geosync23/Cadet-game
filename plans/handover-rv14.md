# Handover: RV14 (code reviewer), 2026-10-25 ~10:00 UTC

**Role:** reviewer under Lead 36 (session_015LyT1p2Kivp1eaMBC7dMQi; before: Lead 34, Lead 35). Notes-only branch
`claude/review-rv14`; full log `plans/review-rv14.md` (every verdict, sha, plant, result). Never change the game.
Verdicts (PASS / FIXES NEEDED, sha + game sha256, what it does, checks, plants, sign-offs) to the lead, copy the builder.

## Verdicts given
- 0.92.5 item 19 Cook-along in the galley: PASS 7ff6a818. Section 8c crewDetail line (80dff612): PASS.
- 0.92.5 item 16 weekend traditions, switched ON: PASS 3307ded5 (perf flags expected, told BM16).
- 0.92.6 FX17 traditions (items 2, 3, 4, 5, 7, 8, 13, 15; P926_TRADS): PASS fa4c1d38; section 19 lines signed off.
  Re-look of 173f21ed (cardWhere(e): the tradition's own rooms + the tap room): see the log's last line for the result.

## Next (for RV17): FX22's appointments (0.92.6 item 9), claude/p926-fx22 582a3544 (game 1389038c...), P926_APPT / ?appt
Built on FX17 4eab8c9f; FX22 still has to merge FX17 173f21ed and staging's promo-sight.lines (lead 36 sends the final sha).
Read plans/handover-fx22.md and DEV_NOTES "Appointments as small traditions". What to watch:
- **Cards closing**: section 18's meetingsTick closes any dialogue with no `where` at the next ship minute (FX22's find).
  apptScene calls `cardWhere()` with NO argument -> only the room you tapped from: tap the host from a doorway, walk in,
  the card closes. After merging 173f21ed it should pass the booking's event (cardWhere(e)). Probe: plans/rv14-probes/cards4.py
  pattern (put the player next to the host, tap, step 20 frames x 24, print DIALOGUE.id each time; and once from outside the
  room). cards.py / cards2.py: the same for FX17's four cards.
- Hooks outside the slot (each `P926_APPT &&`): eventsTick apptFrame, eventJoin apptJoin, tradJoinable (appointment one-offs),
  evOneOffDefs (`only`, `appt`, `toBed`; absent = as before), the Appointments app, the Record. Off must be cadet_test
  ALL IDENTICAL vs 53c11f88 (rerun once if a_start alone differs: a timing flake, backlog FX17-2).
- Save: SHIP.apptx saved only with the switch; check a save/reload mid-booking.
- Planner purity: bookings reach the planner only as one-offs (eventOneOff), as player invitations already do.
- Plant one fault per appt_check part and see each FAIL its own line (the review rule). appt_check has its own "planted" part.
- Words: content/appointments/*.appt baked by content_gen's new parse_appt; content_gen --check; lines_check.
- appt_check on 582a3544 was running when I wrote this (/tmp/rv14/a926/appt.txt; container-local).

## How I test
- Setup: plans/testing-guide.md 2.0. A worktree of the branch (/tmp/rv14/wk); builds in /tmp/rv14/b; each run its own CADET_WORK
  with three symlinked; two browser runs at once (three makes page loads time out: join_check died twice that way).
- Background runs: run_in_background with timeout up to 2 h (the 30-min default kills long checks).
- Switch-on copies: sed "s/^const P926_TRADS = URL_FLAGS.has('p926')/const P926_TRADS = true/" (P926_APPT: 'appt').
- Part of a check: the file up to its first `with sync_playwright() as pw:` plus the part, `__file__` set to the real check.
- Probes in plans/rv14-probes/ (exec cadet_test.py's head; run with CADET_WORK set): hosts926.py (each new tradition's host
  planned at each showing), old_trads.py (old traditions unchanged between two builds), cruz63.py (a person's plan that day).
- Gotchas: never pkill -f a pattern in your own command line (use the [x]yz trick); a builder's "check passed" once came from
  a check that never parsed: always run it yourself; Vance is "he"; Calder is "she"; food_check 7 'garden, good' FAIL is old.

## Open questions for the user
None from me.
