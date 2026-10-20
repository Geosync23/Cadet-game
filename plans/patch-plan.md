# Playtest patch plan: summary (revision 3, final)

The page with all the details, screenshots and the open question is `plans/patch-plan.html` (shots in `plans/patch-plan-shots/`, probes in `plans/patch-plan-probes/`). Planned by PP1 for lead 20 on claude/integration 5dd740c (0.64.2 + slots), at phone size 390×844.

**Revision 2 (2026-10-20)** adds the user's answers (db `answers/patch-plan`, 12:52 UTC) and reviewer PR1's review (`plans/patch-plan-review.md` on claude/patch-plan-review 77d930e, with lead 20's calls). The patch is built after Dev mode.

27 of 28 reproduced. #25 is wording only. #13 and #18 were confirmed from the code and words, and #17 is partly reproduced. About 21 turns in six batches. **Every question is answered; the plan is final** (the user, 2026-10-20: pp-v3-q1 bar only, pp-v3-q2 20 minutes). `pp-v3-general` stays open for a last comment.

## Build order

| Batch | Items | Turns | Regressions |
|---|---|---|---|
| A. Day 2, the first solo job | #1, #2, #28 | ~2 | intro only, except #1's desk swap (Deck 5 crew: day_check, cadet_test) |
| B. The arrival evening | #3, #4, #14, #15 | ~1.5 | intro only |
| C. Training day | #11, #12, #17, #13, #18, #19 | ~3.5 | intro only; #17's tap-path part gated or proven identical |
| D. The crew's life | #7, #9, #10, #8 | ~4 | crew plans change: day_check and cadet_test differences checked one by one |
| E. Small features | #25, #21, #6, #24, #5, #30, #29, #26 | ~8.5 | each new feature behind its own switch; the mug (#30) before the bar (#29) before the tradition (#26) |
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
| #29 | Cocoa only at the bar, plus free at First Light Cocoa |
| #30 | Walking about, you keep the mug about 20 ship minutes, then you've drunk it |
| #26 | First Light Cocoa (idea 1 with the tips from idea 3), plus cocoa at the bar (#29) and the mug in your hands (#30) |

## Found in passing

Backlog #15: the goal arrow lowercases a name ("zeke Torres", 15b line 14872).

## Revision 3 (2026-10-20): First Light Cocoa, cocoa at the bar, the mug

- **#26 First Light Cocoa** (the user: "Mix 1 and 3. Mostly just the tips from 3. I like 1. Also need a cocoa at the bar and you can see the mug in your hands.").
  - When and where: `when: arrival monday`, 20:00-20:45, the bow lounge, after Gym club.
  - The flow: Mail the evening before, a reminder at the end of the shift, Zeke's invite at dinner, tap to join. The intro's bed arrows wait until it's over.
  - What happens: the lounge dims; Dev Raman (Senior Helm Officer, the pilot who flew you in) shows where the Wren has been and where she's heading; cocoa goes round; three of five long-serving crew (Holt, Kowalczyk, Brennan, Halloran, Sato) give a first-day tip, all true in the game except Holt's chair, the user's example; Tomas (a week aboard) and then you say one thing you've noticed (three replies); mugs up. No pin gift.
  - Words: drafted in `plans/patch-plan-first-light-cocoa.md` (the .trad and the .meet, for the writers). New pieces for the traditions engineer: `ties: meeting`, `anim: cocoa`, an invite from a non-host, the lounge dim; for the dialogue engineer: `? pick 3`. 1½ turns.
- **#29 Cocoa at the bar.** It already exists: `BAR_DRINKS.cocoa` (15, line 13835), 2 credits, 17:30-23:00, drunk at a stool (`ixDrink`: hunger +10, social +4, leisure +5, +6 with company). The fix: cocoa (and tea) in a mug (#30), leisure +8 for cocoa, its own serve line; the kettles stay tea (decided: bar only). Player engineer, ¼ turn.
- **#30 The mug in your hands.**
  - Built on the holds the game has (`HOLDS`, 8b line 46669: toolbox, datapad, tray, crate, cart, device) and the prop kit (`PROP_KIT`, 8b line 46878).
  - A cream mug with the cocoa 0.005 below the rim and a handle overlapping the wall (nothing coplanar), at about 1.6× life size: about 8 px tall at the phone's usual zoom (50 px a tile), instead of 5.
  - Held one-handed at the chest; at a stool the drink pose shows the mug instead of the glass; the crew at the tradition hold mugs too (packed into the crowd's meshes).
  - Held until you sit and drink it (20 ship min), put it down, or after about 20 ship min walking (decided). You keep it in the lift. Picking up anything two-handed finishes it first. A reload clears it, as today.
  - The game has one camera (third-person, orthographic), no first person: checked at phone size at zoom 1.5 and 0.7.
  - Mock-up probe `mug.py`: draw calls 180 → 182 while held; shot `30-mug-mockup.png`. Performance engineer (8b) and player engineer (15), 1 turn.
