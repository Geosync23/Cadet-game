# Playtest patch plan: summary

The page with all the details, screenshots and the user's questions is `plans/patch-plan.html` (shots in `plans/patch-plan-shots/`). Planned by the patch planner PP1 for lead 20, 2026-10-20, on claude/integration 5dd740c (0.64.2 + slots), at phone size 390×844. The patch is built **after Dev mode**; each item says how Dev mode's day jump and tradition start test it. Lines are at 5dd740c (`python3 tools/section.py --where LINE`).

27 of 28 reproduced. #25 is a wording change, so there was nothing to reproduce. #13 and #18 were confirmed from the code and words, and #17 is partly reproduced. About 19 turns in six batches. 17 questions for the user (`pp-q1`..`pp-q17`, plus `pp-general`), each with a recommended answer.

## Build order

| Batch | Items | Seats | Turns | Regressions |
|---|---|---|---|---|
| A. Day 2, the first solo job | #1, #2, #28 | Onboarding, writers, player | ~1.5 | intro only: identical at test URLs |
| B. The arrival evening | #3, #4, #14, #15 | Onboarding, writers, player, HUD | ~2 | intro only |
| C. Training day | #11, #12, #17, #13, #18, #19 | Interactions, player, sim, writers, onboarding, traditions | ~3 | mostly intro only. #19 moves the Works crew on Day 1. #17's tap-path part is gated or proven identical |
| D. The crew's life | #7, #9, #10, #8 | Sim, crew designer, deck architect, performance | ~3.5 | crew plans change: day_check and cadet_test differences, checked one by one |
| E. Small features | #25, #21, #6, #24, #5, #26 | HUD, social, device, player, Works career, deck architect, rec, traditions, writers | ~7 | each new feature behind its own switch |
| F. Needs tuning | #16, #20, #22, #27 | Player | ~2 | numbers only. player_check expectations are updated in the same turn |
| (note) | #23 | events plan | n/a | not built in this patch |

## Each item in one line (the cause, then the fix)

- **#1** The Chief's Day 2 appointment has no spot in her office. `introPlan` (14, 10518-10531) skips the desk and the office's event places, so she stays in Main storage. The meeting is also only open 08:45-09:00 (21, 39207), and the shift starts at 09:00. The red-haired person is Marta Soto, given the office desk `5-office-1`. Fix: her spot is `5-office-stand-1`, the meeting is open 08:45-10:00, it starts when both of you are there, and you're walked to the visitor's spot (standing: "Come in. Don't sit."). Tried on a scratch copy.
- **#2** "first job" appears in section 19's `DEV_BEATS['d2-solo']` (10909: Schedule, heads-up, Tracked), `calder.lines:138`, introChief.meet (gist and line 13), and 21's stand-ins (39189, and 39543, which also has the wrong time "Ten to eight"). Fix: "first solo job" in all of them.
- **#28** The `t:laund2` tip may only show 06:00-09:00 on Day 2 (15, 12389). Fix: due whenever you're awake and not clocked in on Day 2, with a second wording for after the shift starts.
- **#3** Since 0.71.3 Calder is seated before you arrive (21, 39176-39179; 14, 10529). Fix: she eats at a nearby table, then walks over on "Look who's coming over" (`crewComeTo`), and her meeting starts once she's seated.
- **#4** "…Then the evening's yours" is in the introDinner meeting, which plays in the panel. The goodnight after the Chief leaves is already a bubble, but only 2 bubbles show at once (8b, 47596). Fix: writers move the lines into `walk.goodnight.1..4`; the crowd's chatter is held back while Zeke speaks.
- **#14** `deviceLockLook` (15, 13245) only changes the button's look. Fix: a glow and a "Tap your device" pointer until the first open (`SHIP.device.booted`).
- **#15** `walk.wing.6` "Laundry there…" is said in the north corridor; the laundry is on the south one. Fix: new words.
- **#11** A tracked arrow never clears itself (15b `trkTap`, 14923), and the intro's arrows wait for it (21 `introArrowTick`, 39939). Fix: a tracked arrow clears once its event has started with you there, or is over.
- **#12** Zeke is "talking" nearly all training day (21, 39817), so he never shuffles aside (15, 13480), and you need the 2 s push (`PUSH_MS`). Fix: an escort in follow mode shuffles even while talking.
- **#17** `escortStep` (10, 48728-48751) parks Zeke on the tile the arrow sends you to, with no gap. Tap paths ignore crew (48195). Fix: he stops about 0.9 m short and takes the tile beside you; a tap that ends on crew stops next to them (gated or proven identical).
- **#13** `t:devwork` (15, 12388) fires on any on-shift moment. New words: "While a long job's bar fills, you can open your device: check your Schedule, Mail or Tracked. The work carries on." It waits for a long work step to be under way.
- **#18** Nothing is written for the end of training day; Zeke's small talk "Ten more minutes with the coils. Breakfast in five." (torres-zeke.lines 376) isn't tied to a time of day. Fix: `? time:morning` on that line, and a new end-of-day moment: "Good job today…" / "Tomorrow you're on your own…".
- **#19** Name on the beam runs 17:05-17:40, after the shift. The arrow aims at the beam's centre (18, 34743), not the top-left slot `BEAM.slots[0]` (3.4 m off). Fix: aim at the slot, and on Day 1 run it from 16:45 inside the shift, with Zeke leading you there.
- **#7** Marrow spends 11.3 h/week on Deck 4 (other officers 3 h): her music habit (14, 9197) plus her musician story at .55 of evenings (10185). Fix: drop the habit and lower .55 to .15, keeping Thursday's piano → 3-4 h.
- **#9** About 130 toilet visits a day but only about 16 reach the stall: visits last 3-6 min (14, 9958) and same-deck walks aren't timed (9896). Fix: a walk lead from fixed map distances.
- **#10** Crew walk tile centre to tile centre at one speed, blind to each other (10, 48642). Fix: a seeded sideways lane (drawing only) and a ±6% speed spread.
- **#8** The stall light is a merged green box, `KM.vacant` (4b, 1434). Fix: its own piece per stall and a red material, switched by who holds the stall.
- **#25** `DECK_NAMES[2]` (11, 49658) reads "Officers' quarters and science". Deck 2 holds both. Fix: the user's wording (pp-q1).
- **#21** The card shows role and friendship only (20, 38027; 19, 11370). Fix: a rank word table, leaving out ranks the title already gives.
- **#6** "Clock out" redraws in the same spot as "Clock in", and so does the early-out confirm (20, `clockScreen` 37056). Punches are final at once (`careerClock` 37026; −2 work rep before 17:00). Fix: a tap guard and buttons set apart, plus Undo (recommended) or Confirm.
- **#24** No menu: shelves hand you "the next thing" (`storePick` 15, 12716). There are 19 goods in `STORE` (12707). Fix: a "Buy something" button on a storekeeper at the counter, opening a menu that feeds today's pay step.
- **#5** The ladder hatch isn't on its deck's service list (4c, 3159), nothing handles the tap, and "Tier 2 access" is written into the texts (4d/4e). Fix: a Spine ladder panel like the lift's, landing tiles, a Deck 5 ladder, the tier words out, behind `LADDER_ON`. Which sealed rooms open: pp-q5.
- **#26** Day 1 has Sunrise stretch, Name on the beam and Gym club, but nothing shows the whole flow until Tuesday's Spice shelf. Monday's Mail is silent on Day 0 (18, 34522). Fix: a new short Monday-evening tradition in the bow lounge with Pell (Settling-in's teacher), with the Mail, a dinner invite and tap to join.
- **#16** A Tier 1 repair holds 45 ship min (75 s), and "Restless" (0.73.0's work leisure drain) makes it 50. Proposed: a player-only Tier 1 factor .67 → 30 min (50 s).
- **#20** Hunger drains 4/h whatever you do: 62 at 17:00. Proposed: 7/h while working → about 38.
- **#22** Social drains 1/h, but meal company (+.2/companion/min), chats and talks keep it at 95. Proposed: drain 2.5/.5, company .1 → about −12 a day, like fitness.
- **#27** `SLEEP_GAIN` 12.5/h: 100 after any 7-8 h night. Proposed: a third of the rate above 85 → 100 only after about 9 h.
- **#23** An inventory of today's big gatherings. Proposed: one all-hands moment per ship-wide event, for the events plan.

## The questions (recommended answer first)

1. #25: which deck and wording? **Deck 2, as the user wrote it** (or "Officers'").
2. #26: Monday or the arrival evening? **Monday, bow lounge with Pell.**
3. #6: undo or confirm? **Undo.**
4. #24: what the shop sells. **Today's 19 goods and hobby supplies.**
5. #5: which sealed rooms open. **The ladder, Engine control and the Sensor array; the Reactor sealed for safety.**
6. #5: does climbing cost energy? **Yes, 2 energy and +1 fitness a deck.**
7. #16: Tier 1 repair. **30 min.**
8. #20: hunger at 17:00. **About 38 (7/h at work).**
9. #22: social. **About 12 a day.**
10. #27: waking at 100. **Only after about 9 h.**
11. #7: Captain on Deck 4. **Thursday plus about one evening.**
12. #3: how the Chief joins. **She walks over from a nearby table.**
13. #4: which line, and how. **The day-runs lines move into the goodnight bubbles.**
14. #14: the device button. **A glow and a pointer.**
15. #19: beam time. **16:45, with Zeke.**
16. #21: the junior rank's word. **"Crew".**
17. #23: large-group moments. **One per ship-wide event, in the events plan.**

## Found in passing

Backlog #15 (new): the goal arrow lowercases a name ("zeke Torres", 15b line 14872).
