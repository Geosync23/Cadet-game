# Handover: FX1, the arrows and tracking fixer (Pillar 5 Steps 1-2 guidance)

Written 2026-10-22 by FX1 (session_01WmdPR5B5QC56Hid3F5M1wv). Lead: lead 28 (session_01S7AdxK1ZyXiEFowP3k5gng), before
that lead 27 (session_017UHW78qnvRTQwYpDxpodHz). Reviewer: AR2 (session_015pnwa5oK7TDF5gZXNFLLvx). Build master BM13
(session_01ExFoVfhiFG3wYTFv2QrojC) sets build numbers; never touch GAME_BUILD or the header's build line.

## Branch and commits
`claude/p5-fix1`, from claude/integration 2b4a05db (0.64.15). This session may push only there.
- 1433e5f: fixes #1-2 (tracking after a job; the training meeting's arrow window). Full set passed.
- the lifecycle commit (after 1433e5f): every career arrow clears, tracking stays on, On shift, clock out with a job,
  the empty board, the shower arrow, lessons not before 09:15, the round waits for clock-in, Tracked names trainings,
  the light relays' tap. Rows for both under "patch-p5-fix1 (FX1)" in plans/build-table.md (they say what and where).

## What moved off me (lead 27, ~12:27)
Bugs 3 (drill), 4 (scanner training), 6 (Tuning words) went to FX2 (claude/p5-fix2); 5 (small lessons) to FX3
(claude/p5-fix3). My work on them was never pushed: it's a patch in my scratchpad only, described to lead 27 in a
message (the drill as ixSideJob in ixChore/ixJobStep/ixHold; the scanner's look-first via scanTrainLook in jobBegin,
scanTrainGoal in ixJobStep, worksPassed in worksDone; worksBrief; {time} in works.ask.m4/m5). Ask lead 27/28 if FX2/FX3
want it re-sent.

## How the pieces work (15b slot, 24p slot, small edits elsewhere)
- `trackFresh()` (15b slot, every frame from ixFrame): a tracked job that's no longer yours -> track undefined.
- `trainArrow(c, now)` (24p slot, from trainTick): the meeting arrow from 15 ship minutes before (with a job in hand, a word 10 minutes before instead: intro_check part 14), "Wait here: ..." in
  its room, down once it starts or is over; state on the function (trainTick can run before the slot's line).
- `goTo(g, key)` (15b slot): a device "go" goal with trk 'go:<label>' (cleared on arrival by trkDoneCheck's place rule);
  nothing sets track = null now except the Jobs/Tracked switch on your own job (and On shift's row when it's on).
- `onSim('newGame')` (15b slot): track undefined, no goal.
- Career goals carry trk fields so 15b's trkDoneCheck clears them (24f Meet Ines, 24p summons/move/ceremony/test job,
  24c's 14:50 drill arrow: trkTo only, FX2 owns the drill).
- Tracked: On shift today is `work: true` (trkOn/trkTap handle it: your job's arrow); ties put the shift row last;
  19's devItemGoal/apptWhereName read 'deck|room' places; trainOffer gives the occasion a title with the teacher.
- 15b ixJobStep: "Shift over: clock out at the time clock" from 17:00 while clocked in (not Day 1 with the intro on).
- 15b `boardEmptySay(empty, now)`, asked by ixWorkStep: one toast each time the board runs dry, not again within the hour.
- 15b roundGuide: waits for clock-in, only while the board offers the round; holding another job, that job's arrow leads.
- trainArrow gives the arrow back to the meeting once a borrowed arrow clears (A.lost reset when IX_GOAL is null).
- 15 needGoal: "someone's own" judged on the place's own deck (`theirs`).
- 15 jobTap: the machine itself by its name within MACHINE_NEAR + 1 (the light relays).
- 24 core trainOffer: never before DAY_SHIFT[0] + 15 (09:15).

## Testing
- `python3 career_check.py BUILD --fx` runs only parts (p) and (q) (two fresh pages, about 1 minute each). Both fail on
  2b4a05db, pass on the tip.
- interactions_check: the Tracked lines and the round arrow test were updated for "tracking stays on" and clock-in.
- AR1's arrows_check (claude/arrows-plan): `shift` and `week`. Its shift clock-out line reads careerClockedIn, which
  stays true after clocking out (told the lead: it should read careerClockedOut). The week stalls on FX3's lift job and
  FX2's drill until those are merged; with FX3's 73cc175 applied my trace got to the light relays (fixed).
- My scratch runner (not in the repo): snapshot the tracked files, check_fast, then mech, career, player, intro --week,
  machine, intro, interactions, devmode, puzzle and day_check 2-8, three at a time, each in its own CADET_WORK.
- Machine: 4 cores; three browser checks at once is the limit (load ~15).

## Loose ends / open questions
- "Wait here" in the meeting's room was my call (the lead's brief said "clears when you arrive"; clearing let the job's
  arrow lead you off before the meeting). Ask the user if they prefer it to vanish.
- A missed meeting's notes Mail ("Your first round is on the board") is still wrong when it isn't (AR2's item; not on
  lead 27's second list).
- The galley plant calibrate chore's pin (arrows_check shift: "nobody yet").

## Handed on
- The Day 8 "Your bunk, Deck 4" arrow up over 3 hours (AR1's arrows_check week) goes to FX3 (lead 28). What I know:
  two things set that label, neither cleared by my work: section 15's needs arrow (`needGoal('energy')`, NEED_FIX_SAY
  "Your bunk"; it clears only when energy is back above WARN_REARM or you start fixing it, so a tired player who works
  on keeps it all day) and section 20's sick arrow (around `setGoal({ deck: deckOf(bed.id), room: bed.room, label:
  'Your bunk' })`, with the infirmary's). I haven't traced which one fires on Day 8. Tracked's own "Your bunk" place
  clears on arrival (trk 'place:bed').
