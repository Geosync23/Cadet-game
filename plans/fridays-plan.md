# Short Fridays and the Captain's address: summary

The page is `plans/fridays-plan.html` (questions `fp-q1`..`fp-q7` and `fp-general` in `form#answers`; save to db `answers/fridays-plan` (revision 1) and `answers/fridays-plan-v2` (revision 2)). Planned by PP1 for lead 21, 2026-10-20, from the user's decision:

> "Friday is good. Let's make it so everyone gets off work early on Friday. Get off at 1530, then meeting at 1600. Then dinner at 1700. We need dialog explaining the short work day Fridays."

The first address is Friday Day 5. It's a separate plan from the playtest patch (about 8 turns), all behind `SHORT_FRIDAY` (off = identical).

## Facts it rests on (lines at claude/integration)

- **Shifts.**
  - `SHIFTS.day = [540, 1020]` (14, line 9180). The day shift's end is set in one place, `schedFrame` (line 9741). Friday's `WEEK_SHAPE` (line 9187) is only `{ late: 30 }`.
  - `eventFree` (line 10393) keeps anyone on shift until 17:15 out of events, so a 16:00 event needs the earlier end.
  - The garden is already 07:00-15:30; the storekeepers and the galley have their own hours. Nothing keeps the bridge staffed after 17:00 today.
- **Meals.** Dinner is already 17:00-20:30 (`MEALS`, line 9179). The galley cooks from 14:30 to 16:30, and the bar preps 15:00-17:00 (`GALLEY_SHIFTS`, line 15255). food_check pins 10 portions at 17:00 and waits of at most 25 minutes in busy windows. The mess has 44 seats and 22 benches.
- **Your clock.**
  - `CAREER` (20, line 36896): in from 08:00, out from 17:00, early-out before 15:00 (−2 work), the miss line at 12:30, auto sign-out at 18:00.
  - `DAY_SHIFT = [540, 1020]` (17, line 17305) is read in about 25 places.
  - leave_check's Friday (Day 12) is only a "missed by 12:30" case. career_check's steady player works 08:00-17:00 every workday.
- **Friday traditions.** Works Friday tea 18:45, the Music jam 19:45, Tap night 20:00, Sunrise stretch 06:30, New hands' tea 18:40 (Day 5), Four weeks aboard 18:40 (Day 26), Crew welcome tea 18:40. **Nothing runs between 15:30 and 17:00.**
- **Mechanics.** Team jobs: Fridays 14:00 in even weeks (`TEAM_FRI`, line 44981), the only Friday-afternoon mechanic. The arrival week: `d5-mug` 13:00 Day 5. "Crossing the Line" is in the events plan, not the game yet (claude/events-plan f6996d86, `plans/events-plan.html`: Sunday Day 7, not a Friday), so fp-q6 covers ship-wide events on a Friday.
- **Existing pieces.** `captainAddress()` (18, line 35495) is a broadcast only (banner and Mail). `rec-all-hands` is the season's all-hands: the first Monday of each season, 17:45, in the auditorium. It stays.
- **Gathering spots** (4d, line 7209+): Deck 3 plaza and promenade 70, the bow lounge 60, the mess 22 plus seats, the Deck 5 bay 108, the auditorium 76 seats. perf_check has no all-hands scene; the closest is the storm party, 60 crew on Deck 3 peaking at 393 draw calls.
- **Who's aboard.** 74 crew (59 day, 15 night). On a Friday 50 day-shift crew are working and 13 are off by rota. Expect about 60-70 at the address.
- **Dev mode.** The excuse rule (12:30) is unchanged. The Clock tab's "To 16:55" (line 50424) needs a Friday "To 15:25".

## Parts, owners, turns

| Part | What | Owner | Turns | Checks |
|---|---|---|---|---|
| A | The crew's Friday: `WEEK_SHAPE` Fri `end: 930` read by `schedFrame`; the worked window and `eventFree` follow; garden, store and galley hours; the skeleton (fp-q2); the night shift about half | Sim engineer | 1½ | day_check (Fridays: Days 5 and 12), events_check, cadet_test (a Monday: identical) |
| B | Your clock: a shared `dayShiftEnd(d)` (17:00, or 15:30 on Fridays) asked of the systems engineer first; clock-out from 15:30 and auto sign-out at 16:00 on Fridays (fp-q7); early-out 15:00, miss 12:30 and leave unchanged; Friday team jobs fit by 15:30; the device's Schedule row | Social engineer (section 20) with Works career; systems engineer (17); device engineer (19) | 1½-2 | leave_check, career_check (Fridays 08:00-15:30), mech_check, machine_check, interactions_check, device_check |
| C | The address: `captains-address.trad`, weekly Friday 16:00-16:25, at the plaza gathering (fp-q1), Marrow at the lead spot with Vance. Who: everyone 90%, night shift 50%, skeleton never. Bubbles with the chatter hushed, plus the banner and a Mail for anyone not there (fp-q3). The same shape each week: the week behind (read when she speaks), welcomes and goodbyes, a department's turn, the week ahead, sometimes you (fp-q5). An event on a Friday makes it the briefing (fp-q6) | Traditions engineer, writers, dialogue engineer | 2 | events_check, join_check, lines_check, content_gen --check |
| D | Dinner: unchanged at 17:00; the cooks keep cooking; each attendee's dinner time spread over 17:00-17:45 (seeded); food_check gains a Friday case | Galley engineer | ½-1 | food_check, events_check |
| E | Explaining it: a line in Zeke's goodnight on Day 0; the Captain's Thursday 18:00 Mail on Day 4; Halloran at 13:00 on Day 5; the Friday time clock screen and the 15:20 heads-up; your name in the first address; Friday breakfast lines | Writers, onboarding engineer, device engineer | 1 | intro_check, lines_check, device_check |
| F | Dev mode: "To 15:25" on Fridays; the address can be started from the tradition list | Dev mode engineer | ¼ | devmode_check |
| G | A perf_check scene: the plaza on a Friday at 16:10 with about 65 crew, at zoom 1.5, 0.7 and landscape (budget 450) | Performance engineer | ½ | perf_check, deck_check |

**Order.** A and B together, then C and D, then E, F and G. The page suggests building it after the playtest patch and before the first ship-wide event, so the events plan treats Friday 15:30-17:00 as taken. design-doc.md changes in the same commit: the shifts table, the weekday shapes and the weekly traditions.

## Questions (recommended first)

1. **fp-q1, where:** the Deck 3 plaza and promenade. Alternatives: the Deck 5 bay, the bow lounge, the rec auditorium.
2. **fp-q2, who keeps working:** a small skeleton (helm and watch ratings on the bridge, a medic on call, the dinner cooks). Alternatives: only the galley; nobody.
3. **fp-q3, how it plays:** bubbles over the crowd, plus a banner and a Mail. Alternatives: the dialogue panel; banner only.
4. **fp-q4, skipping it:** nothing bad (the Mail). Alternative: a small work reputation dip.
5. **fp-q5, what she says:** a fixed shape with parts that change. Alternatives: short and fixed; mostly news.
6. **fp-q6, a ship-wide event on a Friday:** the address becomes its briefing. Alternatives: skipped; both.
7. **fp-q7, the Friday auto sign-out:** 16:00. Alternative: 18:00.

## Revision 2 (2026-10-20): the user's answers

| Question | Decision |
|---|---|
| fp-q1 Where | **The rec deck auditorium** (76 seats and the lectern; about 60-70 come, so all can sit) |
| fp-q2 Who keeps working | A skeleton: helm and watch ratings on the bridge, a medic on call, the dinner cooks |
| fp-q3 How it plays | Bubbles over the crowd, plus the banner and a Mail. The user's comment: "Need to write interesting, fairly substantial addresses that take us through the progression. 3 or 4? Or do the math" |
| fp-q4 Skipping it | **Expected:** missing it gives a small work-reputation dip (the size of being late; set with the Works career engineer). No dip on leave, sick, a rota day off, a Dev-mode excuse, or on nights (Pillar 5's Day 19) |
| fp-q5 What she says | The weekly shape with parts that change |
| fp-q6 Events on a Friday | **Both happen** |
| fp-q7 Friday sign-out | 16:00 |

**What the auditorium and "both" change:**
- **The address runs 16:00-16:40** (it was 16:25). 12-16 lines at one every 5 real seconds is 60-80 real seconds, which is 36-48 ship minutes.
- **The ride up to dinner:** the crew leave the auditorium in seeded waves, ride up to Deck 3 (some to Deck 4 to wash first), and their dinner is spread over 17:00-17:50. The sim engineer checks the rec deck's lift queue with about 60 leaving.
- **perf_check scenes:** the auditorium at 16:10 with about 65 seated, and the rec lift lobby at 16:42.
- **The four addresses**, outlined on the page for a writer seat:
  - **Day 5, welcome aboard:** your first week, Crossing the Line on Sunday Day 7.
  - **Day 12, steady in the storm:** the ion storm (Days 11-15) is on; your Officer promotion (Day 10).
  - **Day 19, after the storm:** the all-clear (Day 14), the comet (Day 16), the commendation (Day 18), Senior Officer (Day 16), your night shifts from tonight, the new junior on Day 21.
  - **Day 26, four weeks, and guests:** the career's end and the Veyli visit's warning.
  - Each address has a fixed core plus slots filled from what really happened (read when she speaks, never by the planner), with a version for a player who's behind.
- **"Both":**
  - Day 12: the address is the Captain's storm update, and a storm phase between 16:00 and 16:40 waits for the address (or the address waits for an emergency phase).
  - Day 26: the address refers to the visit's warning, which keeps its own time.
  - The events plan's F0 marks Friday 15:30-17:00 as taken.
- Parts C and E now read "the auditorium". About 9 turns.

**New question:** fp-v2-q1. Day 12's address falls during the storm, and the storm was settled with no auditorium all-hands. Recommended: hold it as usual in the auditorium as the regular Friday address. Alternatives: ship's speakers that week; the plaza that week. Plus fp-v2-general.

`design-doc.md` is updated in the same commit: the shifts section (Short Fridays), the weekly traditions (the Captain's Friday address) and the weekday shapes (a short Friday).
