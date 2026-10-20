# Review of the ship-wide events plan

Reviewer ER1, 2026-10-20. Reviewed: `plans/events-plan.html` / `.md` / `-run-log.json` on `claude/events-plan` (f9431a62), against build 0.64.2, `design-doc.md`, DEV_NOTES and the Pillar 5 plan v11 (`origin/claude/p5-design`). Everything below was checked in the code or by running the game on scratch copies at phone size (390 × 844). The game file was not changed. Screenshots are in `plans/events-review-shots/`.

## In plain words (for the user)

The plan gets the big picture right:
- The career ends on Day 26 with "Calder's question".
- The three events before that are the ion storm, comet viewing and the diplomatic visit.
- The storm is built but needs bringing up to date.
- A shared base should be built once and reused by every event.

Most of the storm problems it lists are real; I made 12 of the 14 happen myself. But four things need fixing before you're asked to decide anything:

1. **The dates it recommends can't happen as the game is built today.** The game picks each event's day by its own rules (a gap after the last event, a person who must be at work, only one event at a time). Under those rules:
   - The comet lands on Monday Day 22, not Sunday Day 21.
   - The visit lands on Day 26, or Day 33 once the comet is in.
   - It can't start on Day 22 as the plan says.

   The plan needs a piece of work for "fixed dates" that it doesn't count.
2. **Two of its recommended answers contradict each other.**
   - Moving the storm a day later (question 2) makes its commendation arrive on Day 17. That's after the Day 16 ready-room scene that question 7 wants to fold it into.
   - The move also doesn't clear the promotion days: it lands Calder's storm briefing on your Officer ceremony day, and the tail of the storm on your Senior Officer day.
3. **The storm test that question 5 is based on was played by a cadet who skipped work.** That's why it came out "rough" and why Calder sent a "My office" letter: it was a missed-shifts telling-off, not a storm result.
   - Left alone, the storm comes out rough every time.
   - Even a perfect ship can't come out "smooth" with today's numbers.
   - Nothing you do in the storm changes the result yet.

   So "helping can make it smooth" isn't true yet; making it true is new work.
4. **The plan's page shows five broken pictures.** Its screenshots were never saved to the branch.

I also found things the audit missed:
- Reloading the game in the middle of a meeting loses that meeting for good.
- The storm is what moves film night to the rec deck, so switching the storm off for testing breaks film night.
- Commander Vance is off duty on the visit's greeting day and its first dinner.
- Your Day 26 mentoring needs a new junior who arrives on Day 21, the comet's evening.

**My verdict: a good plan that needs one more pass before you see its questions.** There are 4 blockers, 17 things that should be fixed and 8 small ones (nits), all listed below. My estimate is about 32-42 build turns, not 26-33. Questions 2, 5 and 7 should be reworded, and four questions are missing (end of this note).

---

## Ratings

**Blocker:** must be fixed before the plan goes to the user. **Should fix:** fix in the plan's next version. **Nit:** small.

### Blockers

**X1. The recommended calendar can't be produced by the event scheduler, and the plan doesn't count the work to make it so.**
- How the game picks a start day (`eventDueDay`, starship-cadet.html:35415):
  - The next event in `EVENT_ORDER` comes at least `gap` days after the last one ended (default 7).
  - Then a hash adds 0 to `spread − 1` days (default 3).
  - Then it moves on to the first day the `need` people are at work.
  - Only one event can run at a time (`SHIP.event`).
- Run in the page (scratchpad C/cal.py; fork A agrees):

  | Case | Due day |
  | --- | --- |
  | today, storm | Day 10 |
  | visit after the storm (Days 10-15 or 11-16), draft lifted | **Day 26** (the plan says "about Day 25") |
  | storm with `earliest: 11` | Day 11 (fine) |
  | comet (pasted from `comet-viewing-draft.js`) after the storm | **Day 22, a Monday**: `need: ['sato']` and Sato works Monday to Friday, so it can never fall on a Sunday |
  | visit after the comet | **Day 33** |

- The plan's "Sun Day 21 (the draft's own date)" was true at 0.34.18 and isn't now.
- The comet's `days: 2` puts its afterglow on Day 22. That's the same day as the visit's warning, which the one-event slot can't hold.
- **Fix:** add a framework piece, call it F0 "the event calendar": fixed start days (or `earliest` with `spread: 1` and the right `gap` and `need`) for all three events, written out and checked by F7. Also decide whether a short event can overlap a main event's warning, or make the comet one day long. About 1-2 turns.

**X2. Questions 2 and 7 contradict each other, and question 2's move doesn't remove the clash it's meant to fix.**
- The commendation and debrief are sent when the afterglow ends (`t >= end`, :35450), at the start of `startDay + days`.
  - Storm on Days 10-15: Day 16 00:00.
  - Storm on Days 11-16 (question 2): Day 17 00:00. That's after the Day 16 Senior Officer ready-room scene that question 7 folds the commendation into, and the same day as the Captain's table toast.
- After the move:
  - **Day 11, the warning:** Calder's 09:15-09:27 briefing runs into Pillar 5's first team job at 09:30 (v11 M8: "Day 11's training"). It falls on the officer ceremony day (17:15). The plan's "after the morning" isn't in the data: the warning phase is 06:00 and the briefing 09:15.
  - **Days 15-16, the afterglow:** these now cover the Tier 3 test (Day 15) and the Senior Officer promotion (Day 16). That's the same complaint item 1 makes about today's dates, which cover the Day 15 test.
  - **Sunday Day 14, the all-clear meeting:** it lists Calder, who is off on Sundays (fork A, `isWorkDay`).
- **Fix:** frame question 2 as a real choice with its costs:
  - (a) keep Days 10-15 and let F1's career-beat guard keep the hours apart (briefing 09:15, summons 11:00);
  - (b) the one-day move, with the briefing after the team job and a shorter afterglow (`days: 5`);
  - (c) another start day.
- Send the commendation at the all-clear (the design says commendations come in the afterglow), so question 7 works whichever date is chosen.

**X3. Question 5 and item 9 rest on a player who skipped work, and the band model can't give the recommended answer.**
- The run log's "15 10:00 Chief Ines Calder: My office" is `career.mail.chief` (:27944), the **missed-shifts** summons, not a storm letter (fork A).
- In every hands-off run, "My office" came on Day 10 13:00 and the Captain's reprimand on Day 15. A cadet who keeps skipping is let go on Day 20 (fork B2).
- What the runs show (forks B1 and B2):
  - **Hands-off is rough every time on paper,** with 1-hour, 6-hour and 24-hour steps and sleep-only skips. It doesn't flip. "Bumpy" only appears when a long skip misses the calls score.
  - **The calls thread is a fixed formula** (`stormCallBacklog`, :35202): the owed crew × 40 minutes ÷ the booths. It comes out at 6, exactly its "rough" line, and nothing the player does changes it.
  - **Blackout minutes are rough at almost any power.** A blackout hour has chance .15 + .45 × (1 − power/100), and each lasts 37.5 minutes on average (`blackoutHour`, :17877), over a 28-hour escalation. At full power that's about 157 minutes, so "smooth" (≤ 60) is out of reach even for a perfect ship, and 200 is passed whenever power is below about 87. The plan's "many more machines" is only part of it: the 0.4 × lowest-machine term.
  - **Spoiled meals count from the warning day** (:15706, any `eventNow`): 10 were spoiled before the front.
  - **The storm prep jobs feed no thread at all.** They only count toward the commendation (grep: they're read nowhere but `mine.jobs`).
- So "Helping can make it smooth" (question 5) isn't true of this build.
- **Fix:**
  - Redo item 9 and question 5 with a player who works their shifts.
  - Say plainly that a smooth result needs new design: prep jobs that lower a thread (ballasts → fewer blackout minutes, batteries → shorter blackouts, a booth rota → calls), threads that count from the front, and blackout odds tuned so full power is smooth.
  - Then ask the user about the outcome. Count it as storm work (1-2 turns), not "retune and check 5 seeds".

**X4. The plan page's five screenshots aren't on the branch.**
- `events-plan.html` loads `events-plan-shots/1-…png` to `6-…png`.
- That folder isn't in commit f9431a62 (`git ls-files` shows none), so the user's page shows five broken images.
- **Fix:** commit the shots, or drop the images.

### Should fix

| # | Finding | Evidence | Fix |
| --- | --- | --- | --- |
| S1 | **Day 26 is a target, not a proven date.** career_check's busy run stops at Day 8 and never reaches a promotion, so it doesn't "confirm Day 10 for both". The code does keep a busy player from Officer before Day 10: `promoAnnounce` :45784 (Day 8, "Relied on", m6) and test day ≥ 9. But Pillar 5 v11 sets no day floor for the Tier 3 and 4 tests, and Officer reputation starts again at zero. A steady new Officer would need "Relied on" in about 2.5 workdays to make the Day 15 test, against 5 as a Junior. | fork A; p5 lines 51, 89, 388 | Ask Pillar 5 steps 5-6 to build day floors (Tier 3 test ≥ 15, Tier 4 test ≥ 22) and a reachable reputation pace, and say the events are tied to the calendar, not to these beats. |
| S2 | **The slow player is wrong.** Officer comes on about Day 29 (test passed Fri 26, summons Mon 29), not Days 25-28. A cadet who skips work is let go on Day 20. | career_check lazy run; fork B2 | Correct the numbers; say rank-aware parts must cope with a Junior, and with no player at all after being let go. |
| S3 | **"Event day" must be defined narrowly, and named `eventDay`.** The head-scratcher code already calls `eventDay(d)` (:43839), which doesn't exist, so the guard is dead. Incidents and team jobs only avoid the party day (`incShipEvent` :44741). If "event day" meant every day of an event, the 6-day storm and 9-day visit would take 15 of Days 11-30 away from puzzles, incidents and team jobs, including P6, P7 and P8's first days (22, 23, 25) inside the visit. | code | F1: name it `eventDay(d)` (true only for onset, escalation and resolution, or for days with an all-hands moment) and agree the meaning with the Pillar 5 seats. |
| S4 | **A reload in a meeting loses it for good.** Reloading at line 3 of 10 of Calder's briefing brought back no panel, no choice and no gist Mail; `met:` is saved, the open dialogue isn't (`meetingsTick` :35608). The same happens for the all-clear and occasions. | fork B2 run | Add to F4: re-show the meeting, or send its gist, after a reload. |
| S5 | **A long skip:** item 5 is right, and worse. One jump from Day 9 to Day 17 starts and ends the storm in a single call: no addresses, Mail, scores or traces, and it comes out "smooth". | fork B1 run | F4 must replay every phase up to the end before ending. Add the jump to F7. |
| S6 | **Item 3 is only partly right.** Calls home are blocked only when `phase === 'onset'`, and for *any* event (`homeCallable` :38932, crew moments :38706), so the visit's greeting day would cut calls too. Nothing reads `commsDown`. This build has no home Mail or "Outside" news to block (none in 14 days). | fork B1 run | F8 reads `eventMod('effect','commsDown')`, not the phase. Drop "home Mail and Outside news" or mark them future. |
| S7 | **Item 4 is partly wrong.** Day 13's Schedule **does** show "19:00 All-clear party". What's missing is the 09:15 briefing and the 10:00 all-clear meeting. Tracked at the front offers "The call booths", which are closed (screenshot B2-2). | fork B1/B2 runs | Correct item 4. F3 should list meetings and hide closed places. |
| S8 | **Item 6 is overstated.** The player's drill and inspection only apply to a Junior (:42387, :42360); a steady player is an Officer by Day 10 11:00, so only slow players are affected. | code, fork B1 | Reword. The puzzle and incident guard (S3) is the real gap. |
| S9 | **Item 7: the rec deck is tied to the storm in a way the plan misses.** The storm's first address calls `recFirstAllHands` (:35474, :34121), which moves film night to the auditorium "from this Saturday", the party night. So the Day 13 clash was made by the storm itself, and switching the storm off for testing means film night never moves. There are also two film-night flags (`rec.film.moved` on the baked one, :33275, and `rec.filmMoved`, :34021); only the second is ever set. Blackouts skip Deck 7 on purpose (`n !== 7`, a lead's call in 0.83.2), and adding it would change every blackout's deck (regressions). The crew already stay off the rec deck on Days 11-12 (0 people at 19:30). | code, fork B1/B2 | Unhook the rec deck's first all-hands from the storm (its own date), flag the two film-night flags to the rec seat, and check the 0.83.2 decision before "include it in the blackouts". |
| S10 | **Item 8 is worse than stated.** The jobs go up at 08:30 and the crew have claimed three by 09:00, before the 09:15 briefing. The "held for you" path only works at posting, so the briefing choice can never hold anything. | fork B1 run | Post the storm jobs when the briefing ends, holding the one you chose. |
| S11 | **Item 13 isn't a storm effect.** With the storm off, the same skip runs out of filters on Day 7 and cells on Day 9. It's the on-paper skip (no supply carts). | fork B1 run | Drop it from the storm list, or move it to the test notes. |
| S12 | **Item 12 misses scenes.** The missed-shifts scenes use the same ready room: Calder's "My office" and the Captain's reprimand at 11:00. | fork B1 | Count them when folding (question 7). |
| S13 | **The comet cancels Sunday traditions.** With the comet on Day 21, `eventPauses` drops Lap of the Wren (20:30) and Talent night; the plan says Lap "ends just as it starts". | scratchpad C run | Correct it, or start the comet's onset after 21:15. |
| S14 | **People off duty on event days.** Vance (off Wednesday and Thursday) is in the visit's greeting cast (Wed Day 24) and off for the first dinner (Thu Day 25) and Pillar 5's Day 17 toast. Calder is off for the moved all-clear (Sun 14). | fork A `isWorkDay` | Check the casts against the rotas in F7, or move the days. |
| S15 | **Day 21 brings a new junior.** Pillar 5 M25 (Day 26 mentoring) needs a junior "who arrived with Sunday's crew rotation". No rotation is due before Day 35 (`ROSTER_ROTATIONS` :48058), so p5:710 brings one from the reserve on Sun Day 21, the comet's evening. | p5 plan | Mention it; decide whether the arrival rides on the comet evening or the rotation tradition (new question below). |
| S16 | **The visit is longer than the design allows.** The design says events run "over 2-4 ship days". The visit runs warning to farewell over Days 0-7, about twice that, and it's 9 days with the afterglow. Question 3 only asks about "past Day 26". | design-doc "Shape" | Ask about the length itself (new question below), or shorten it. |
| S17 | **Phone checks.** `perf_check` has no storm scenes. The party is 236 / 367 draw calls (portrait / zoomed out), not one 307. A blackout in Deck 4's junior common room zoomed out reads 454 against the 450 budget (an ordinary Friday there already reads 452). | fork B1/B2 | F7: add the front, a blackout and the party to `perf_check` SCENES; flag the 452 to the performance seat. |

### Nits

- **N1.** Item 2's count of 89 storm lines is exact (48 with one cue, 41 with two). The visit has 2 more. Confirmed, so F2 holds.
- **N2.** Item 10 is confirmed: on phones the banner covers the HUD and the Tracked title (B1-10, B2-1, B2-2). On the test clock it stayed up for days.
- **N3.** Item 14 is confirmed: the stand-ins (:35472, :35503, :35625) are unused; only the framed menu has no prop.
- **N4.** `ADDRESSES` and `FEEL_DONE` aren't saved. A reload inside the front's 3-minute window could replay the jolt.
- **N5.** Day 13's evening has three traditions plus the party, over the two-an-evening limit.
- **N6.** Tiles and Lightdisc stop the clock, so a player can sit out the front or a blackout in a game. A blackout only changes the lights.
- **N7.** The plan's "13 vs 22 on Deck 3" doesn't match its own log ("crew3": 8). career_check fails on 0.64.2 (busy "Relied on" on Day 4): pass it to the career seat, as the plan says.
- **N8.** With both events switched off nothing is ever due, so Dev mode must start events with `eventStart` (F6 assumes this; fine).

### Confirmed as written

- The career dates for a steady player: Officer Day 10, ceremony Day 11 17:15. The Pillar 5 v11 table for Days 15-26 matches.
- There's no Tier 3 or 4 code yet.
- Item 1's clash: the warning lands on the Officer summons day.
- Item 5: a skip from Day 12 to Day 16 drops the all-clear, the calls score and the afterglow.
- The visit's cabins: Teshavi in 2-U (the second visitors' cabin, not the suite Pillar 5 gives you), the other three in 4-01 to 4-03.
- Every dressing and trace id exists, except the framed menu's prop.
- Two fresh runs are identical with the rec deck on, and the storm never calls `R()`.
- Clothes and laundry aren't touched by the storm.
- The visit's four threads have scorers.
- **Possible:** a game reloaded four times through the storm ended at 352 blackout minutes, against 405 in unbroken runs. Not isolated; F7 should test "a reload mid-storm gives the same result".

## The shared base (F1-F8): is it the right base?

Mostly yes. Changes:
- **Add F0, the event calendar** (X1): fixed days, the one-event slot, short events beside main ones, and casts checked against rotas.
- **F1** must be `eventDay(d)` with a narrow meaning (S3), plus the career-beat list.
- **F4** covers reloads inside meetings (S4) and jumps from before the start to after the end (S5), not only long skips.
- **F7** adds the reload test, the jump test, the cast-on-shift check and the `perf_check` scenes (S17).
- **F8** reads `commsDown`, not the phase (S6).
- **New, inside the storm update:** the threads the player can move (X3).
- **Leave F5 (rank) small.** Writing lines for each rank is the head writer's work and isn't counted. Say who writes the comet's and the visit's new lines.

## The turn estimate

26-33 is low. My estimate: F0 +1-2, the player-moved threads +1-2, the meeting reload and the rec deck unhooking +1, and the visit 10-12 rather than 8-10. The visit needs the escort walking, the Veyli look, the dinners with choices, the senior briefing, draw calls on Decks 1 and 2, and all of the storm's updates again. **That's about 32-42 turns**, plus the writers' time, which sits on the path.

## The questions

| # | Is it the right question? | Change |
| --- | --- | --- |
| 1 The list | Yes. | — |
| 2 Move the storm | Wrong as framed: the move only shifts the clash (X2). | Give options (a), (b) and (c) with their costs. |
| 3 The visit past Day 26 | Too narrow (S16). | Also ask about its length (new question A). |
| 4 Calendar, not rank | Right. | Add that a slow player may have been let go by Day 20 (S2). |
| 5 The outcome left alone | Based on wrong evidence (X3). | Re-ask after a run where the player works; say what helping will change. |
| 6 Close the rec deck | Missing facts. | Under the move, the closure is the whole weekend (Fri 14:00 to Sun 10:00). The storm also starts the rec deck's first all-hands and film night (S9). Recommend unhooking it first. |
| 7 Fold the ready rooms | Breaks under question 2's move (X2). | Send the commendation at the all-clear; count the missed-shifts scenes (S12). |

Missing questions:
- **A. The visit's length.** It's about 8 days aboard against the design's 2-4. Shorten it to about 4 days (greeting, one dinner, farewell), or keep it?
- **B. The new junior on Day 21.** Should the Day 26 mentee arrive at a small crew-arrival moment on the comet evening, or should a short "crew rotation day" move before Day 26?
- **C. What can you do in the storm to change how it goes?** For example: fit the ballasts and the lights hold longer, run the booths' rota and the queue shortens. This is a design choice the user hasn't seen.
- **D. (for the lead, not the user)** Should a short event be able to run alongside a main event's warning? Without it the comet and the visit can't be a day apart.

## How this was checked

- **Career dates:** career_check on 0.64.2 (fork A); the career code at :45784-45863.
- **The scheduler:** runs in the page (scratchpad `C/cal.py`): `eventDueDay` under each change, rotas from `isWorkDay`, the comet draft pasted in.
- **The storm:** run hands-off and with a player at 390 × 844 at 1-hour, 6-hour, 24-hour and 10-minute steps, with jumps of Day 12→16 and Day 9→17, with the rec deck on and off, the storm off, and four reloads (forks B1 and B2; scripts in the reviewer's scratchpad).
- **Draw calls:** portrait zoom 1.5 and 0.7, and landscape.
- **Screenshots** in `plans/events-review-shots/`:

  | File | Shows |
  | --- | --- |
  | `B1-10-front-banner-390.png` | the banner over the HUD, with the missed-shift panel under it |
  | `B1-party-d13-z1.5.png`, `B1-party-d13-z0.7.png` | the party (the old banner is still up: the test clock) |
  | `B2-1-front-hud-deck3.png` | the front |
  | `B2-2-tracked-onset.png` | Tracked offering the closed booths |
  | `B2-3-blackout-deck4.png` | a blackout on Deck 4 |

---

## Re-review of version 2 (claude/events-plan 15d04602), for lead 20

The checks behind this re-review were run in the page (scratchpad `C/v2.py`): the comet set to Day 16 at 21:30 for one day, the traditions on Days 16-26 with and without it, and who is on shift on Days 19-27. Version 2 took in all of X1-X4 and S1-S17 correctly. The findings below are tied to the question each one affects.

- **Q2 (storm vs the first promotion): agree with (a), keep Days 10-15.**
  - Under (a), and under (b)'s shorter afterglow, the storm ends at Day 16 00:00, so the comet on Day 16 fits beside it in F0's one-event slot.
  - Option (c) (Days 17-21) collides with the Day 17 toast, Vance's days off on 17-18, and both night shifts. If the user picks (c), the comet and the visit must move too, and the page should say so under (c).
- **Q3 (the comet): agree with Day 16 at 21:30.**
  - Checked: no tradition that Tuesday is cancelled. Tiles night and Knit and natter end at 21:30, and `eventPauses` tests the minute before the end.
  - Sato is on shift. Vance's 17:00 walk is long over by 21:30.
  - The draft's gatherings must be re-registered for the new date: `EV_SHIPWIDE` is built when the game loads, so a comet added later draws nobody. That's a build note, not a question.
- **Q4 (the visit): don't recommend Days 19-26. Recommend a short weekend visit on Days 26-29, as the career's hand-off on purpose.** Four problems with Days 19-26:
  1. **It takes Pillar 5's whole Tier 4 week.** With version 2's own narrow `eventDay` (front, escalation and all-clear), every day from 22 to 26 is an event day. That means no head-scratchers, incidents or team jobs in the week when P6, P7 and P8 first appear (Days 22, 23 and 25) and the puzzle rate rises to 1 in 3. M24, leading a team on Day 25, is itself a team job, and team jobs skip event days (`teamBusy` → `incShipEvent`, :44977).
  2. **The warning falls on the night-shift weekend.** Calder sends you home at 13:00 on Friday Day 19 to sleep (p5:355), and you work the nights of Days 19 and 20. The "weekend jobs" and Vance's Mail come while you're asleep or on nights.
  3. **Days 22, 23 and 26 are crowded.**
     - **Day 22:** the greeting would follow the Monday briefing and the Tier 4 test, which is held 09:00-15:00 if it works like Tier 2's.
     - **Day 23:** the dinner is the same evening as the Engine Specialist welcome.
     - **Day 26:** a whole day of mentoring, plus the gift exchange at 09:00, the farewell at 10:00 and the debrief, then Calder's question. Day 26 also has no Works Friday tea (four-weeks-aboard takes 18:40; checked).
  4. **It still runs 8 days from warning to farewell (Days 19-26),** against the design's 2-4. Only the time aboard was shortened.

  **Better:**
  - The Day 22 Monday briefing names the visit as next week's business (an F5 senior memo). This keeps question 1's "pays off the Senior rank".
  - Vance's warning Mail comes on Friday Day 26 after Calder's question.
  - The greeting is Saturday Day 27 at 10:00, with one dinner Sunday Day 28 and the gift exchange and farewell Monday Day 29 at 10:00. The afterglow is Tuesday Day 30.
  - Vance works Days 26-30 and Marrow works on Day 29. Weekend meetings work without the cast on shift: the storm's all-clear already runs on Saturday Day 13.
  - The event days are then Saturday, Sunday and Monday 29, so the Tier 4 week is untouched. Warning to farewell takes 4 days, within the design. The career's last scene hands straight into the ship's next story ("the ship carries on", p5's "after" row).
  - It runs 3 days past Day 26, so put it to the user as "the finale, on purpose". Ending the visit before Day 22 doesn't work: Days 17-21 hold the toast, Vance's days off and both night shifts, and Day 21 has the new junior's arrival.
- **Q1:** unchanged (yes), but its line "the visit is where your Senior rank pays off" still holds under the Days 26-29 option, through the Day 22 briefing.
- **Q8 (folding scenes):** agree. Under (a) the commendation comes at the all-clear on Day 13. The ready room would otherwise summon you on Monday Day 15, the Tier 3 test day, so folding it into the Day 16 scene is right. Say "no summons on Day 15" outright.
- **Q5, Q6, Q7 and Q9:** no new findings. Q7 under (a): the rec deck is closed from Thursday Day 11 14:00 to Saturday Day 13 10:00.
- **Nit:** in the shift check, `torres` isn't a roster id, so check his rota under his real id before F0's cast check.
