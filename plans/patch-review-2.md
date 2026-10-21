# Patch reviews: PR2

## Handover (2026-10-21 ~03:40 UTC, at about 475k of memory; lead 22's call)

PR2 is idle. PR3 takes the events team's reviews from here.

- **Role:** adversarial reviewer of the builders' turns: the patch builders PA, PB and PE, the events engineer EV1, and the writers EW1 and EW2. From ~03:00 I also covered owner hooks in sections 19 and 20 (OR1 handed over). I report to lead 22 (session_01BGQCZLK6gYTnqu6mwZ61jB). I pushed only to claude/patch-review-2.
- **Everything reviewed is below, newest last. Everything passed.** No review is open.
- **Waiting with the lead or others:**
  - EW2 2a0f57e: the lead's call on Saruth's lantern-supper cord line (lore plan vs the storm brief), and merging its two half-lines.
  - EV1 F0a: the switch-on events_check still expects the Day 10 storm, and quiet-watch day 300 (2 not reached) is unexplained. EC1/EV1 own them.
  - EV1 F3b: the nits (the moved comment, "Days 11-11").
- **Method (what worked):**
  1. `tools/section.py --diff`; the build-number lines untouched.
  2. check_fast in a worktree; cadet_test OLD NEW **alone** (never alongside another check).
  3. For switch-gated work, `sed` EVENTS_ON (or the item's switch) to true in a copy and probe it in-page (scripts in `plans/patch-review-2/`, on PP1's `pp.py` harness).
  4. 390×844 shots looked at.
- **Gotchas:**
  - Bubbles pop in with a real-time CSS animation, so add `.bub{animation:none!important}` for shots.
  - Section 20 applies ship notes when their hour ends (F2b bypasses this for event notes).
  - `pkill -f` on a pattern that matches your own shell kills the shell.
  - intro_check takes 25-40 minutes; give it a long timeout.
  - Content reviews: a helper agent can cross-check facts, but verify its points (it got one wrong: the promoted flag exists).

The playtest patch reviewer from 2026-10-20 ~19:15 UTC, taking over from PP1 (`plans/handover-patch-planner.md` on claude/patch-plan). Reports to lead 21. Owner and hook reviews are OR1's (claude/owner-review-1) since 19:36.

How each review is done (PP1's method):
1. `tools/section.py --diff`.
2. The build-number lines are untouched.
3. check_fast in a worktree.
4. cadet_test BASE→HEAD, alone on the machine.
5. intro_check where the arrival changes.
6. A probe of my own at 390×844, looking at the shots.

Probes live in `plans/patch-review-2/`.

Harness gotcha (new): speech bubbles pop in with a real-time CSS animation (`.bub` → `bubIn`), which never runs under the test's virtual clock. Their card stays at opacity 0 in screenshots although `display` is block. Add `.bub{animation:none!important}` before taking shots.

## PA batch B: claude/patch-a 8ee5d6b (#15, #3, #4, #14). PASS WITH FIXES

- **Checks:** check_fast OK (325 s). cadet_test 4de6dbb→8ee5d6b ALL IDENTICAL (noise only). intro_check parts 1-9 and 11 clean; part 8: "the Chief 0 m from hers at the next table". My run hit its 25-minute limit in part 10.
- **Probe `rvB.py`** (the arrival evening in the real game):
  - #3: the Chief sits at 3-mess-26 [29,4] through the dinner chat, walks on "Look who's coming over", and is seated at 3-mess-9 before introChief.
  - #4: the four goodnight bubbles 18:56-19:02. `introHush()` is true throughout and false 4 s after. No other bubble until 19:06. The bubble is readable at the table (`rvB_goodnight_1.png`).
- **Fix 1 (#14):** from the handover in Bunk 1 (18:16) until the first open, the "Tap your device" pointer covers the needs strip's first three bars, and it shows over the introBunk dialogue (`rvB_pointer_dialogue.png`). Hide it during dialogues and cap it at about 30 real seconds, keeping the glow.
- **Nits:**
  - The `LINES['tip.device.first']` lookup is dead.
  - Positions are written every frame.
- **Note to the lead:** how a day runs is now only said if you're within 6 tiles at the goodnight.

## PE #26 First Light Cocoa: claude/patch-e cf45e2a. PASS WITH FIXES

- **Checks:** check_fast OK (300 s). cadet_test a0bd82a→cf45e2a ALL IDENTICAL (switch off).
- **PE's `e26.py` with `&firstlight&mug`:**
  - Day 1 only, 20:00-20:45.
  - Join: a free cocoa, sit:cocoa, three tips of five (holt, brennan, sato), Tomas, three replies, rel given.
  - The dim: hemi 0.85→0.55.
- **Fix 1 (bug):** `flcTick` calls `bubbleSay(z, line)` with the DECK_CREW record, not its handle `z.h`. bubbles.update reads `w.h` as a height, gets NaN, and the bubble stays `display:none`. Proven in-page: `bubbleSay(z.h, …)` at the same moment shows.
- **Fix 2 (bug):** `FLC_SHOWN` isn't saved, but `SHIP.events.joined` is. A reload in the lounge before 20:45 replays the meeting, and its rel can be earned twice.
- **Fix 3 (plan):** the Day 1 bed arrow shows 19:00-20:00, before the cocoa. Hold it from the invite until the tradition ends.

## PA batch C: claude/patch-a eb638e7 (#11, #12, #13, #17, #18, #19)

- **Checks:** check_fast OK (297 s). cadet_test 8ee5d6b→eb638e7 ALL IDENTICAL.
- **FAIL: intro_check part 8.** The follower and Torres both sit at Deck 5 [6,11] from 17:40 ('haulway') to 19:20, so the table comes at 20:11. After that, no introChief, no goodnight, no bed arrow, and core tour lines 6/18. Batch B's run of the same part was clean.
- Almost surely #17: escortStep's ESC_GAP stand and/or escBeside keep him off his spot, so the step never advances. Sent to PA with fix options.
- OR1's scope note was passed on: #11, #12, #13 and the floor tap act in normal play.
- To do on the fix: intro_check part 8, then `rvC.py` (the end of training day: #18/#19 arrows, Zeke's gap).

## PE #26 fixes: claude/patch-e b3fed46. PASS

- The invite bubble is on `z.h`; my shot `e26_invite.png` shows it by Zeke at 18:21.
- "Shown" is kept in the save as the flag `firstlight.shown`.
- flcBusy runs from the invite until the tradition ends, unless declined (`e.to` is minute of day, correct).
- cadet_test cf45e2a→b3fed46 ALL IDENTICAL.
- PE's intro_check (FLC_ON + MUG_ON, after the fixes): no FAIL in parts 1-11 and 13. The run stopped at its 2-hour limit inside part 12; the timeouts were slowness, not a hang.

## PB batch D: claude/patch-b 2e517ff (#7, #9, #10, #8). PASS

- **Checks:** check_fast OK (307 s). day_check OK. events_check OK. food_check OK.
- cadet_test 5d6ee1c→2e517ff shows differences, as expected: the crew's lanes and plans move the shots and taps. OR1 traced them with switch-off copies.
- **#10:** c10c's longest pair run is 2.5 s (mark: 3 s).
- **#8:** the red cap shows only on the taken stall (30/30 samples). My projected crop `08-red-crop.png`: about 4×2 px at phone zoom.
- **Notes:**
  - The Captain is 4.5 h a week on Deck 4 (the plan said about 3-4).
  - 9 of 35 visits still miss the stall.

## PA batch C re-review: claude/patch-a ffd8ed7. PASS

- **Fixes read:**
  - escToYou (the stop never applies while leading).
  - trkAway (a tracked place clears only after you've been away).
  - The done key `d1-end:told`; d1-end starts at 16:44; the board arrow yields.
- **intro_check --evening:** OK. The dinner chat at 18:39, the Chief 0 m from her next-table seat, her welcome at 18:43, the goodnight said.
- **rvC.py at 390×844:**
  - Zeke follows from 16:46, with a gap of 2 m or more.
  - walk.trainend.1-3 at 16:51, 16:53 and 16:55.
  - The clock-out arrow at 16:56; the beam arrow straight after clocking out, through 17:13 (`rvC_clockout.png`, `rvC_beam.png`).
- **Nits:**
  - "That's the day! You did well." repeats the good-job line just after clocking out.
  - The board arrow stays during his three lines.
- **Still owed by PA:**
  - The batch B pointer fix.
  - #19's dinner nudges.
  - #31.
  - The full intro_check parts 9-12.

## PB batch F: claude/patch-b d3b028f + 6c7be04 (#16, #20, #22, #27). PASS

- **The numbers, against the user's answers:**
  - JOB_PACE .72 on every tier (the 1.25 step kept). The board shows your minutes at that pace; the crew's are unchanged.
  - Hunger 4 + 3 an hour while workingNow().
  - Social [3, .25].
  - SLEEP_TAPER [90, 1/3]. The alarm forecast follows it.
- **Checks:** check_fast OK (282 s). cadet_test 2e517ff→d3b028f ALL IDENTICAL. player_check OK.
- **6c7be04:** the lane eases to the middle while escorting or walking up to you.
- **Judgement calls, passed to the lead:**
  - Tier 1 "Relied on" 40→48.
  - The lower bands come about 1.4× sooner, untested.
  - player_check's steady player now has company at meals and two chats a day.

## PB #31 "Ask Zeke" parked: claude/patch-b 95c22e7. PASS

- **Code:** INTRO_ASK_ON is false. A pending tour extra still plays on a tap; otherwise the tap is taken with no panel. The introAsk path and its lines stay parked.
- **Checks:** check_fast OK (281 s). intro_check part 8 was flipped by PB.
- **`rv31.py` at 390×844:** three real taps on Zeke on the ramp. Each reached introTap (true), with no dialogue, chat card or panel (`rv31_tap1.png`).

## PB 319f541 (revert of 9e34423, the user's call). PASS

- WORK_BANDS is byte-identical to integration 5d6ee1c.
- career_check's spot test is back to 39/40. machine_check's range is 3-7 (6.2 measured).
- check_fast OK (280 s).
- 16df5bd adds #31's reason line in the design doc.

## EW1 event lines: claude/events-lines b8c2ee8 (content review for lead 21). PASS WITH FIXES

- **Clean:** no arc spoilers; the Veyli are always they/them; days, rotas and traditions are correct.
- **Fixes:**
  - "deck R" in Mail/speech should be "the rec deck" / "rec dec".
  - The engineer's note in ionStorm:108's gist.
  - d19:48 (asleep), d19:35 (this week), d12:29 (yesterday), crossingLine:30 ("I'm flying it").
  - {stormjobs}/{myjobs} plurals.
  - {me} lines near 90 characters; the banner ionStorm:60 is 91.
  - New conditions and headers not yet agreed with EV1 (mine.jobs is JS, not a condition).
- **Judgement calls for the user:**
  - d19:41 "Chief Calder has plans for you".
  - d26:47 the surprise after dinner.
  - Crossing the Line's own cake.
- The cross-check was done with a helper agent and its key points verified by me. Its `flag:promoted` finding was wrong: the flag exists.
- **EW1's fixes 407fd07: PASS.** Every fix and the lead's calls are in. Left for EV1: myrank, myshift:night, {leavers} and the .address bake.

## PA fix round: claude/patch-a 75aa54a (batch B fixes, C's #19 nudges, the nits, OR1's 2 s give-up). PASS

- **Checks:** check_fast OK (272 s). cadet_test 0.64.5→75aa54a ALL IDENTICAL. intro_check --evening OK.
- **rvB:** the pointer shows from 18:19 with no dialogue open and is gone at 18:36 (about 30 real s); the glow is kept (`a2_dinner_pointer_gone.png`). The goodnight bubbles 18:55-19:01, hushed.
- **rvC:**
  - The clock-out arrow at 16:52, right after his first line.
  - The beam arrow straight after clocking out (`a2_beam.png`).
  - Zeke's good job only once; Theo Teague gives the clock-out remark.
  - The gap is 2 m or more.
- **Not walked by me:** the owed-goodnight path and its Mail (code read OK; asked PA for a probe line).

## EV1 F0a: claude/events-base 835ab24 (the event calendar, behind EVENTS_ON). PASS

- **Switch off:** check_fast OK (261 s); cadet_test 0.64.5→835ab24 ALL IDENTICAL. The code reads correctly; the load order is safe.
- **Switch on, in a copy:** events_check fails 8 lines.
  - Nearly all are its hard-coded Day 10 storm: the storm day, the all-clear party on Day 13, the routines, the guest days, film night, rec-slow-stretch on Day 14.
  - One is unexplained: quiet-watch day 300, Deck 3, 2 not reached. Sent to EV1.
- **e73bacb:** PA's probe p4owed covers the owed goodnight. Away: a Mail at 22:01 (owed=3). Near at 20:30: the bubbles (owed=2). check_fast and --evening OK after integration came in.

## EV1 F1a: claude/events-base 0313e52 (eventDay, behind EV_GUARD_ON). PASS

- check_fast OK (263 s). cadet_test 835ab24→0313e52 ALL IDENTICAL.
- Pure: reads only the calendar, the phases and EV_SKIPPED.
- Note: it uses the planned day r.day, not the day evCalDue might push an event to.

## EV1 F1b+F1c: claude/events-base 1030626 (the career-beat guard, the summons, the Captain's table). PASS

- **Off:** check_fast OK (267 s); cadet_test ALL IDENTICAL; the occasion times and Mail text are unchanged.
- **On (`guard.py`):**
  - The ready room: Day 10 at 16:00, Day 18 at 16:00, none on the test and captain days.
  - The Captain's table: 19:00+75 before the night shifts (Days 19-20); none on Day 17.
  - The Friday hold and the night shifts are honoured.

## EV1 F2: claude/events-base a2d9f40 (a ship note per phase, behind EV_NOTES_ON). PASS

- cadet_test alone: ALL IDENTICAL, with no noise. check_fast OK (273 s).
- **On (`f2cue.py`):** notes at 14:00 Day 12 (onset), escalation and resolution. The cue event.ionStorm.onset appears once the social hour has run (15:04), stamped 14:00 and lasting 1 day: an hour's lag, by section 20's design.

## EW1 Crossing the Line story A: claude/events-lines 172e556 (for lead 22). PASS WITH FIXES

- **Guard rails hold:** Tomas never touches exams, tests, Holt or staying; Holt has one here-and-now line; Saruth has one line; no cake, no visit spoilers. The reach fact is neutral.
- **Fix:** the ceremony moved to the bow lounge, so every plaza line needs changing: notice.ceremony, job.ribbons, the plaque comment, two onset reactions, Holt's warning line, Zeke's worst-face line, lineLap's "where it happened today" and the ceremony header comment.
- **8e2433b: PASS.** Every plaza line is fixed; the only "plaza" left is the header comment noting the move.

## EV1 F3a: claude/events-base 18f0d9d (code 9ddea29; the event on your device). PASS WITH FIXES

- **Off:** check_fast OK (291 s); cadet_test 0.64.6→18f0d9d ALL IDENTICAL.
- **On (`f3.py`):** the Day 11 Storm briefing at 09:15; Day 14 the all-clear at 10:00 and the party 19:00-21:00; the closed call booths are dropped from Tracked on Day 12.
- **Fixes:**
  - With heads-ups off, devHeadsTick skips 'event' items while the meeting notify is now null, so there's no notice at all. Let them through like 'beat'.
  - The phone shots don't show the event rows; retakes asked for.
- **EW1 dfd083a (story A): PASS.** The Lap stop is at the bow lounge doorway (3-lap-6), so "This is where it happened today" is right again.

## EV1 F0c: claude/events-base bb285a0 (code 8b0c8dc; SHIP.evFrom, evCalPlan, the readers). PASS

- **Off:** check_fast OK (280 s); cadet_test ALL IDENTICAL; no save key.
- **On (`f0c.py`):** the plan is [ionStorm Day 11]; due is Day 11; eventDay is true on 12 and 13; evSkippedFor(20) is crossingLine, ionStorm, comet. My F1a note is settled (eventDay reads evCalPlan).
- **Nit:** the job readers strip \W, so job ids must stay \w-only (they are today).

## EV1 F3a fixes: claude/events-base d88c78f. PASS

- notify is kept with heads-ups off, so the s19 line needs no change (covered for OR1). The party is listed once. The timed Mail mail.<key>.at is unused today.
- check_fast OK (274 s); cadet_test ALL IDENTICAL.
- The retaken shots show the briefing (Day 11) and the all-clear plus party (Day 14). Nit: the Day 11 shot's HUD says Day 1.

## EV1 F2b: claude/events-base 5189d08 (cues at once; the s20 socHear hook, covered for OR1). PASS

- **Off:** check_fast OK (272 s); cadet_test ALL IDENTICAL.
- **On:** the onset and front cues are there at 14:04 on Day 12. social_check OK on the switched-on copy (play and jump agree).

## EW2 Veyli lore: claude/events-lines-2 bd69395. PASS, with one decision

- Every user decision is applied: human, "went on", "your people"/"the Concord", own pronouns everywhere, nothing named, the description rule.
- No spoilers (six hours, Saruth's reason, the visit). Lore steps by tier.
- lines_check: only "not baked" (expected).
- **Decision for lead 22:** two Saruth lines in Crossing the Line's afterglow, against story A's "one line" rule.
- **712d8e8, why the crossing matters (line-q10 A): PASS.** The guard rails hold; `!who:saruth|holt` is supported; the Mail is 316/400. The Saruth fold isn't in yet.

## EV1 F3b: claude/events-base 1c86ab4 (Home's status line, Record's events; the s19 hooks covered for OR1). PASS

- **Off:** check_fast OK (271 s); cadet_test ALL IDENTICAL.
- **Shots:** the status line on Home (3 lines at 360, fine: keep 60); Record: "Ion storm, Days 11-16" with its band.
- **Nits:** the moved 0.34.51 comment; "Days 11-11" for a one-day event; the staged HUD day.

## EW2 storm story A "Sixty by lamplight" (2a0f57e) and the Saruth fold (8ccd97c). PASS

- **The fold:** one Saruth line (tier<acquaintance gets the courtesy line, >= the lore line).
- **Storm A:** the guard rails hold (Lukas: covers only; Brennan: "his galley tonight" only, none of her story; no late or short supper).
- **The lead's call:** Saruth's lantern-supper cord line versus the brief's "nothing about the Veyli" (the lore plan put it there). Its two half-lines should be merged.
- **Nit:** several reaction bubbles are over the brief's 60 (under lines_check's 90).
