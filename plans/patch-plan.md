# Playtest patch plan: summary (revision 2)

The page with all the details, screenshots and the open question is `plans/patch-plan.html` (shots in `plans/patch-plan-shots/`, probes in `plans/patch-plan-probes/`). Planned by PP1 for lead 20 on claude/integration 5dd740c (0.64.2 + slots), at phone size 390×844.

**Revision 2 (2026-10-20)** adds the user's answers (db `answers/patch-plan`, 12:52 UTC) and reviewer PR1's review (`plans/patch-plan-review.md` on claude/patch-plan-review 77d930e, with lead 20's calls). The patch is built after Dev mode.

27 of 28 reproduced. #25 is wording only. #13 and #18 were confirmed from the code and words, and #17 is partly reproduced. About 20 turns in six batches. **One open question:** `pp-v2-q1`, which one-off tradition runs on your first Monday, plus `pp-v2-general`.

## Build order

| Batch | Items | Turns | Regressions |
|---|---|---|---|
| A. Day 2, the first solo job | #1, #2, #28 | ~2 | intro only, except #1's desk swap (Deck 5 crew: day_check, cadet_test) |
| B. The arrival evening | #3, #4, #14, #15 | ~1.5 | intro only |
| C. Training day | #11, #12, #17, #13, #18, #19 | ~3.5 | intro only; #17's tap-path part gated or proven identical |
| D. The crew's life | #7, #9, #10, #8 | ~4 | crew plans change: day_check and cadet_test differences checked one by one |
| E. Small features | #25, #21, #6, #24, #5, #26 | ~7.5 | each new feature behind its own switch |
| F. Needs tuning | #16, #20, #22, #27 | ~2 | numbers; player_check expectations updated in the same turn |
| (note) | #23 | n/a | for the events plan |

## What revision 2 changed

- **#1 (the review's blocker).** Calder's Day 2 appointment is at her own desk: `5-office-1` becomes hers, and Marta Soto gets another Works desk. The appointment starts 20 minutes early. That's a per-appointment `early` field passed from section 21 to 14, a shared format, so it goes to the sim engineer first. Her block ends when the meeting is done. The window is 08:45-10:00 and counts as work time. The meeting starts when both of you are there. The fallback only runs at 09:15, or 20 minutes after you arrive, which is longer than her 14-minute walk. You stand ("Come in. Don't sit.").
- **#7.** The evening chance goes .55 → .15 for the Captain only: `captain ? (thu ? 1 : .15) : .55`. Done for everyone, it would have halved Mbeki and Ueda. Her "music" habit is dropped in `plans/crew-roster-gen.py` (only her row may change in the regenerated diff).
- **#9.** The walk lead comes from `DECKS` place tiles (distance × a detour factor, at the slowest speed; never live paths). The stall is held from arrival, because Deck 4 has only 2 toilets for about 59 visits a day. Pass mark: c9 re-run, most visits reach the stall and dropped visits don't rise.
- **#10.** The fix is now: people leave the lift about 0.5 s apart; a walker within 0.45 tiles of a same-way walker ahead matches their speed; a seeded lane eased round corners. Pass mark (c10, Deck 3 at dinner): no pair within 0.3 tiles for more than 3 real seconds. 1½ turns.
- **#8.** A red cap slightly in front of the merged green light, shown only while the stall is taken (draw calls only for taken stalls in view).
- **#6, the user chose "both".** A tap guard and buttons set apart on every punch. An early clock-out (before 17:00) is confirmed, with Cancel where "Clock out" was. Clock-in and a clock-out at or after 17:00 get Undo for 5 real seconds, or until you walk away from the clock. The punch counts at once from a kept copy of the clock record; only its side effects (the remark, reputation, the `clock` note) wait until Undo is gone. A save ends the window first. Owner: the social engineer (section 20), with the Works career engineer reviewing.
- **#19, the user's choice.** Keep 17:05. At 16:50 Zeke says good job (#18), tells you to clock out, and an arrow goes to the time clock. Then the arrow goes to `BEAM.slots[0]` at the beam's height, and the dinner nudges wait. Intro only.
- **#26.** A one-off on the first Monday (`when: arrival monday`), 20:00-20:45, after Gym club. The weekly Monday traditions don't run on Day 1. The intro's bed and call-home arrows wait until it's over. Three ideas for `pp-v2-q1`:
  - **Star call** (recommended): the Deck 3 promenade windows, hosted by Dr. Imra Sato.
  - **Cocoa round:** the junior common room on Deck 4, hosted by Tomas.
  - **Your mug on the hook:** a new mug rack in the mess, 18:40-19:10, hosted by Brennan.
- **F, the overall result.** The tuning is measured with all four of the user's numbers together (`fnet.py`, a steady player's week on paper with the game's own needs code, task speed read every 15 minutes of each shift):

  | Tier 1 repair on a normal shift (ship min) | Bed 22:00 | Bed 23:00 | Keeps to themselves |
  |---|---|---|---|
  | Today | 40.7 | 40.8 | about 45 |
  | The four numbers, no repair change | 41.2 | 42.1 | 45.8 |
  | With ×0.67 | 27.6 | 28.2 | 30.7 |
  | **With ×0.72** | **29.6** | **30.3** | 33.0 |

  The factor is **0.72** (the user's 30 minutes, about 50 s). It applies to all of the player's tiers, keeping the 1.25× step (a Tier 2 repair is about 37 minutes overall). The job board's minutes (17, line 18300) use the same factor, and the systems engineer reviews.
- **Career pace.** Experience, credits and job-kind skill come per finished job, so they arrive sooner where the board has work. The training rows are day-gated, so their days don't move. Dev mode's "Set career" table should be measured after batch F.
- **#22.** Drain 3/.25, company unchanged: about 18 a day in a quiet week. A steady player with calls sits at 67-90. Someone who keeps to themselves hits 0 by Day 3. "In good spirits" now covers 85-90% of shift time.
- **#27.** A third of the sleep gain above 90: 8 hours gives 100, and bed at 23:00 gives 93-96. "Well rested" covers 21% of shift time instead of 33% after a 23:00 bed.
- **Nits from the review, all taken:**
  - #3 is ½ turn: the walk-over code exists (`calderGo`, 40040-40046).
  - #4's hush is reviewed by 22 and 8b.
  - #14's pointer never exists at test URLs.
  - #11 clears by kind: meeting, tradition or appointment once started with you there or over; job when taken or done; place on arrival.
  - #12's pass mark: past him in under 0.5 s.
  - #17: the escort keeps his own pace.
  - #13: the tip waits for a long hold on any day of the first week.
  - #28: a late-wake wording ("clock in first").
  - #20: the skipped-breakfast case.
  - #24: one builder (player engineer), the others review.
  - #5: Deck 5's hatch goes in a wall slot, with deck_check and day_check on Decks 2, 5 and 6.
  - #25: the user's capitals and dash, as written.
  - "Six batches" is fixed on the page.

## Decided (the user, first round)

| Item | Decision |
|---|---|
| #25 | Deck 2, "Officer's Quarters - Science" as written |
| #6 | Both: confirm an early clock-out; Undo for the rest |
| #24 | Today's goods |
| #5 | Ladder, Engine control and Sensor array open; the Reactor sealed. Climbing: 2 energy, +1 fitness a deck |
| #16 | 30 min |
| #20 | 7/h at work |
| #22 | About 18 a day |
| #27 | 100 after 8 h (slower above 90) |
| #7 | Thursday plus about one evening |
| #3 | She walks over |
| #4 | Goodnight bubbles |
| #14 | Glow and pointer |
| #19 | Keep 17:05; Zeke holds you from 16:50, tells you to clock out, arrow to the clock |
| #21 | "Junior Officer" |
| #23 | In the events |
| #26 | A different new tradition: pp-v2-q1 |

## Found in passing

Backlog #15: the goal arrow lowercases a name ("zeke Torres", 15b line 14872).
