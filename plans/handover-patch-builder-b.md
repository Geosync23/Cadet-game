# Handover: patch builder B (PB), 2026-10-20

**Role.** Sim engineer for the playtest patch (`plans/patch-plan.html`, final): I own sections 13, 14 and 10 (ship time and saving, the crew's schedules, the crew walking). My new code is in the slot `// ---- slot: Sim engineer (section 14)`. I report to lead 21 (session_01KYPEbF745ZQ9g9kr4XJgre). PR2 (session_013ttt3gV3DaF9y4caBtFnh9) reviews the patch, and OR1 (session_01W7AHxrcgBM3rJNtCFKwp9W) stands in for the section owners.

**Branch.** `claude/patch-b`, from `claude/integration` 0.64.4 (merged in). I haven't changed the build number. check_fast was OK on every push.

## Done
- **Batch D**, reviewed and passed by PR2 and OR1:
  - #7: the Captain's music habit dropped through `plans/crew-roster-gen.py`; her other-evening chance is now .15. The generator first had to be brought in line with hand edits made to section 9.
  - #9: a toilet trip's walk (`walkLead`, 1.6 times the straight line) is taken out of the end of the activity before it, at most half of it; nearest stall first.
  - #10: crew step out of the lift one at a time; a walker closing on someone ahead going the same way takes their pace; each walker has a drawn-only lane (`walkGap`, `walkLaneStep`, `liftOutOk`).
  - #8: the stall's red cap (`stallCapAdd` and `stallCapsTick`; hook 1d8d606 in 4b).
  - Details: DEV_NOTES "The playtest patch, batch D".
- **Batch F**, passed by PR2 and OR1:
  - #16: `JOB_PACE` .72 on your machine jobs.
  - #20: `WORK_HUNGER` 3 an hour extra at work.
  - #22: social drains [3, .25].
  - #27: `SLEEP_TAPER` [90, 1/3].
  - Hooks: 22c4442 (17, the job board) and 9e34423 (24, Tier 1 "Relied on" 40 -> 48).
  - machine_check now allows 3-8 jobs a shift. player_check's paper week has company at meals and chats.
  - Details: DEV_NOTES "The playtest patch, batch F".
- **#10 follow-up** 6c7be04: the escort and walk-up steps ease the drawn lane to the middle.
- **#31** 95c22e7 and the reason commit: "Ask Zeke" parked behind `INTRO_ASK_ON = false` (section 21, PA's); intro_check part 8 flipped; design-doc's arrival paragraph marks it cut, with the user's reason. Waiting on PR2's review.

## Owner reviews I gave (PA's claude/patch-a)
- 47b3dba: OK.
- 155f0d4: OK.
- 6e9e86d: OK with one fix, `if (mine == null || mine === pl.id) continue;` in the schedDesks trade.

## Gotchas
- **Toilet walks:** don't push a toilet visit later. That made days end past midnight, a tradition overrun, and day_check's rec-deck comparison (Deck 3 must never hold fewer people with the rec deck than without, minute by minute) fail by one person. The basin step after the toilet has no walk of its own: giving it one ate the toilet visit.
- **Probes:** `plans/patch-plan-probes/c9c.py`, `c10c.py` and `c8d.py`. They skip drawing (`window.__skip = true`); with rendering on they take more than 20 minutes each.
- **Running checks:** at most 2-3 checks at once on this 4-core box, or pages time out loading (a `Page.goto` timeout is load, not a real failure). Give each check its own `CADET_WORK`.
- **Killing probes:** never `pkill -f <pattern>` when the pattern appears in your own command line; it kills the shell.
- **Timing the game:** the test harness clock is virtual, so `performance.now()` timings read 0. Count the operations instead.

## Loose ends
- **Optional (#9):** more crew go to the toilet after waking (.5 -> .7). Not done.
- **For the lead or the user (PR2 and OR1):** with quicker jobs, the lower Tier 1 ratings also come about 1.4 times sooner, and nothing tests them.
- **Dev mode:** the "Set career" table should be re-measured after batch F.
