# Review: playtest patch 1, parts B, E, F and J (RV3)

Reviewer RV3 (session_01Uct2TvRPoFYViyU1X9Fpjx), branch `claude/review-play1`. All four branches start from claude/integration 32b699a6 (0.64.14, sha256 94f32868...881e9). The plan: plans/patch-playtest1.md on claude/lead-26. For each branch: is the note really fixed (driven in the browser with Playwright), did nothing else change (cadet_test), were the checks run and OK, is design-doc updated, is the look unchanged.

## B. The arrow and the lift (notes 9-12), FR4: claude/patch-play1-b 4d062c45

**Verdict: PASS** (two optional nits, one merge note).

Sections touched: 15b (+16/-5), 11 (2 lines), 19 (1 line), 15 (1 line, the ladder panel). No section 17. No build-number lines.

Driven in the browser (390 x 844, Day 9, a Tuesday after the arrival week, no job):
- Note 9: at 08:10 the marker stands over the time clock, "Clock in at the time clock". Clocked in through the real time clock screen (tap, then its Clock in button): the arrow turns to "Take a job at the job board"; took a job on the board's panel: "Fetch a cable: the Lights shelf" (the job's own steps, as before). From Day 1 with the intro on: nothing (section 21's own arrows), checked on paper.
- Note 10: tracking "Tea and biscuits" in Tracked at 13:00: the goal's point is the tea table's own position (0.55, -7.3), not the middle of the tea corner; the arrow points there.
- Note 11: walking into the tea corner with tea tracked over your job: the arrow goes straight back to the job's step (track back on). With tracking switched off before, it stays off (FR4's check part).
- Note 12: the lift panel's marker reads "→ Tracked" (aria: "What you're tracking is here: The Tea corner, Deck 5"); the spine ladder panel too.
- No console errors.

Checks I ran on 4d062c45: cadet_test against 32b699a6 **ALL IDENTICAL**; check_fast **QUICK CHECK OK** (351 s); interactions_check **OK** (with FR4's new paper part). FR4 also reports intro_check --firsts and --week OK, events_check OK. design-doc: the HUD and Tracked lines updated. Build-table row present.

Nits (optional):
1. After you clock in, the arrow keeps saying "Clock in" until the next ship minute (about 1.7 s at SHIP_RATE .6): ixFrame only recomputes the job step when its key changes, and the key has no clock-in state. Adding `careerClockedIn` to the key would make it turn at once.
2. Stopping a tracked item by hand (tapping its row again) leaves job tracking off, as before this patch; only "done" brings the job back. Probably right, but the note says "after tea"; worth a word in the summary.

Merge notes:
- With D (the Chief's solo job, CJ1): if the solo job on Day 2 isn't `myJob()`, this arrow will say "Take a job at the job board" during it. Check on the merged build (B merges after D).
- With J: see J below (one fix there, on J's side).

## J. Clock-in and clock-out reminders (note 20), CK1: claude/patch-play1-j 1188cbdf

**Verdict: PASS at ec06f68e** (05:05 UTC). First reviewed at 1188cbdf: PASS WITH ONE FIX (below). CK1's ec06f68e changes only that line (`if (typeof trkDone === 'function') trkDone(IX_GOAL); else clearGoal();`) and its build-table row; CK1's check_fast OK (241 s), career_check (l) OK. My re-probe on B 4d062c45 + J ec06f68e merged: tracking "Clock in" from beside the clock, then clocking in, now gives "Take a job at the job board" with tracking back on (was: no arrow, tracking off).

Sections touched: 15 (+108 in its slot, one call in playerUpdate's once-a-minute block), 15b (one line in trkItems, FR4 agreed), 22 (the baked words only, through content/). No build-number lines. No R(); nothing the crew's planner reads; SHIP.player.clockRm saved (about 35 bytes).

Driven in the browser (390 x 844, Day 9, no job, not clocked in, needs held up so no need arrow; on Deck 3 at first):
- Clock in: "pre" at 08:30 (Tracked: "Clock in 09:00"), "start" at 09:00 (Tracked: "Clock in Now"), "late" at 09:15, "later" at 10:00. Clocked in for real at the time clock: the Tracked row goes.
- Clock out: "end0" at 16:50 with the clock-out arrow, "end" at 17:00; I left Deck 5 for Deck 4 at 17:02: "You left without clocking out. Pop back to the time clock, or it signs you out for you at 18:00." and the arrow says "Take the lift to Deck 5: clock out at the time clock".
- On J alone there's no clock-in arrow (by design: it's B's ixWorkStep); on B + J merged, the clock-in arrow is B's and J's Tracked row sits alongside it.
- No console errors.

Checks I ran on 1188cbdf: cadet_test against 32b699a6 **ALL IDENTICAL** (renderer noise only); check_fast **QUICK CHECK OK** (292 s); career_check: the new part (l) all OK over Days 9-17 (easing off after three good days, back on a slip, the two Mails, the Tracked rows); the only FAIL is the known old `busy: "Relied on" before Day 5` (backlog 12). CK1 also reports intro_check OK twice. design-doc rule added ("Clocking in and out: the reminders"); DEV_NOTES and build-table updated.

**The fix (found on B + J merged, 4d062c45 + 1188cbdf, a test merge; only plans/build-table.md clashes):** when the clock's own goal is done, clockRemindTick calls `clearGoal()`. With B, a goal tracked from Tracked over your job carries `back`, and B's `trkDone(g)` turns job tracking back on; clearGoal doesn't. So: in the Works bay at 08:35 with no job, tap "Clock in" in Tracked (track goes null), clock in: the arrow is gone (track stays null), and B's "Take a job at the job board" arrow never comes. Probed: from far away it's fine (B's trkDoneCheck clears it with trkDone on arrival), but anywhere in the Works bay (the clock's room, where the board is) it's lost. Fix, in J's line `if (typeof IX_GOAL !== 'undefined' && IX_GOAL && /^clock:/.test(...)) { ... clearGoal(); }`: use `typeof trkDone === 'function' ? trkDone(IX_GOAL) : clearGoal()`. Same for the clock-out row.

Notes (no change needed):
- The first morning a day there can be one more toast than the reminders (section 20's own in-bay toast and tips), as CK1 says; they're spaced 5.6 s apart at least.
- Owner review: section 15 is the player engineer's; J sits in that seat's slot. The lead may want PB2 (or whoever holds that seat) to glance at it.

### J, second fix: claude/patch-play1-j 4bc3e39c (07:57 UTC, CR6's clothes_check find in the full round)

**Verdict: PASS at 4bc3e39c.** The 10:00 reminder, held while other toasts were up, fired 2.1 s after the washer's answer toast hid, and clothes_check read the reminder instead of the answer. The fix is only in clockRmHeld: held while `#toast` has `show`, and for CLOCK_RM.gap (10 s) after the 5.6 s stamp; design-doc's rule updated; career_check (l) gains a proof ("an answer toast up, then gone": held, held, then said).
My runs on 4bc3e39c: clothes_check **ALL OK**; career_check (l) OK, including the new line (only the known backlog-12 FAIL); check_fast **QUICK CHECK OK** (341 s); cadet_test against ec06f68e **ALL IDENTICAL**.
Note (no change needed): at SHIP_RATE .6 a ship minute is about 1.7 s, so the 09:00 "start" window (10 ship minutes, about 17 s) is barely longer than the new hold (5.6 + 10 s); a toast just before 09:00 can drop that one reminder. The "you forgot" ones (09:15 and later) still come, so it's fine; worth knowing if the user says a reminder didn't show.

## E. Ladder taps and the rower (notes 14, 16), LD1: claude/patch-play1-e 7e26050e

**Verdict: PASS** (two notes for the lead, one owner look).

The first tip sent, e36549af, had no game change (only the build-table row and two PNGs); LD1 re-pushed 7e26050e, whose game file is sha256 3b33cb34...9d85a9c as reported. Sections: 4b (+14, the rower's mover), 15 (+29, the ladder block: ladderAimed, ladderAt, ladderRoom; ladderTap and ladderStep), 11 (one line in tap()). No map, path or deck data. No design-doc change (behaviour fixes, no new decision). No build-number lines.

Driven in the browser (390 x 844), real screen taps through section 11's tap() at the ladder's rungs, 0.6, 1.5, 2.0 and 2.5 m up, from a few tiles away, on Decks 1-6:
- Note 14: the ladder panel opened **17 of 24** (old build 32b699a6: 1 of the first 14, the rest walked you to the floor). Misses: the 0.6 m taps on Decks 1, 2, 4, 5 and 6 (they land on the lobby's low wall in front, which is a walk as before), and Deck 5 at 1.5 and 2.0 m (the lift brake stands in front and gets the tap: "Lift brake"). LD1's judgement call 2 says so.
- Note 16: rowing on Deck 3's gym rower (you, `sit:row`): the hands move about 0.7 m along the rower over a stroke; LD1's six-frame strip (plans/patch-play1-e/rower-after.png) shows the handle in the hands in every frame (before: drifting out of them). LD1 measured within 0.01 m for you and crowd rowers.
- With H merged (LR1's d0f96def; a test merge, only plans/build-table.md clashes): taps 17 of 24 again; a rung tap on Deck 4 walks you into the ladder room (ladderStand's tile) and opens the panel; climbs 4->2, 2->6, 6->5, 5->1 land on each deck's ladderStand tile, in the ladder room.
- No console errors.

Checks I ran on 7e26050e: cadet_test against 32b699a6 **ALL IDENTICAL**; check_fast **QUICK CHECK OK** (463 s); interactions_check **OK**; player_check **OK**.

For the lead:
1. Deck 5: the lift brake in front of the ladder takes taps at 1.5-2.0 m; only the top of the ladder opens the panel there. Fine by the rule "what's in front wins", but it's the deck the user works on. Possibly revisit after H (LR1) opens the room.
2. LD1 offered a standing ladder-tap part for interactions_check; nothing checks note 14 today. Worth a backlog row (or a small follow-up), not a blocker.
3. Owner: the rower's mover is in 4b (the deck architect's); it reads section 15's ACT.body and section 10's DECK_CREW at run time, typeof-guarded, falling back to the old swing.

## F. Breakfast at 07:00 (note 18), SC1: claude/patch-play1-f dd83d896

**Verdict: PASS at dd83d896** (14:10 UTC; lead 27's review, with the section 14 owner check, PB2 being released). Game code reviewed at 8d65f86f; dd83d896 only changes words (content/ rebaked: Vance's breakfast at 07:05 everywhere and facts.md; "till nine" for four pre-existing "till eight" breakfast lines). Base: claude/integration 2b4a05db (0.64.15), merged into the branch at 85cef096. Still to do on the merged build once BM13 publishes 0.64.16 (Zeke): machine_check's repair share and a cadet_test against 0.64.16 (below).

What changed (sections 4b, 4d, 15, 22: words and signs; 14 and 16: the schedules and the galley): `MEALS.breakfast` [420, 540], `FOOD.open.breakfast` 420; the crew's wake unchanged (05:30-07:15); "straight to breakfast" crew up before 07:00 wait in their bunk till 07:00-07:40; the spread of breakfast times starts at 07:00; the night shift comes off at 06:00, unwinds in the Deck 3 lounge, eats 07:00-07:40, then showers and sleeps; the chef rises 05:30 and cooks from 05:50; the early hands prep 05:30, cook with the chef 06:00-06:30, bake 06:30-07:00, line from 07:00. design-doc.md (the galley's day, a day through three decks, meals) and the build-table row describe this final version (wake unchanged, Deck 3 unwinding), not the earlier later-wake one.

Every item on the 06:00 list above is handled: MEALS, FOOD.open, the galley plans and galleyShift's head, the servery, menu board and both canvas signs, the hunger tips, the closed servery and pans texts, the night shift, the morning spread. Pick-your-own (06:15-06:55, picking in the garden) stays before breakfast, which suits it. The player's alarm stays 06:00. Tomas's Day 1 06:00 wash scene: unchanged and still right (the wake didn't move); its "Breakfast's till eight" line is now "till nine".

**Section 14 owner check** (crew plans read from `planDay`, Days 1, 3, 6 and 9, against 0.64.15):
- 06:00-07:00 is spent in the Deck 3 lounge (about 10-12 people: the night shift and early risers), in bunks (5-12 people, "off"), the washroom and toilets, the gym and the morning traditions (sunrise stretch, pick-your-own, dawn swim). Before, 13-18 people ate between 06:00 and 06:30.
- Breakfasts by half hour (Day 3): 07:00 31, 07:30 19, 08:00 9, 08:30 11, 09:00 2; a short queue forms from 06:47-06:57.
- The night shift eats 07:00-08:00 (was 06:02).
- Nobody uses the early grab shelf before 07:00; not needed.
- day_check Day 1 and Day 3 **OK** (worst stuck 0.0 ship min on every deck; draw calls well under 450); food_check 1 7 **OK** (Day 1: 151 came to eat, longest wait 2 min at dinner, breakfast 0).

Checks I ran on 8d65f86f: check_fast **QUICK CHECK OK** (347 s); food_check 1 7 **OK**; day_check 1 and 3 **OK**; on dd83d896: content_gen --check up to date, names_check OK. machine_check (in check_fast) OK with the steady player's repair share **40%** (17 of 42; 0.64.15: 20 of 40, 50%): deterministic, so no flake between runners; the size of the sampling noise (about 8 points at 40 jobs), not a change in how the crew claim repairs; accepted by lead 27, backlog LEAD27-1 (measure over 28 days).

**cadet_test against 2b4a05db: DIFFERENCES FOUND, all explained.** State: `tris`, the five taps and their walks, state_end; every shot but g_nocrew differs widely (g_nocrew 149 px, max 58). The cause is the crew's moved mornings (the test starts Day 1 06:00 on Deck 4: who is in bunks, the corridor and the washroom at 06:00 changes, and with it doors, what a tap hits and where you walk). Proof: a copy of 8d65f86f with only the section 14 and 16 code hunks put back (all the words kept) is **ALL IDENTICAL** to 2b4a05db.

**Re-check on 0.64.17** (claude/integration-next-0.64.17 1d2f3269 = 0.64.16 b9f053ba + dd83d896, game sha256 22583691...a4c4b5; 14:20 UTC): the merged change is exactly F's own plus the two build-number lines. machine_check **OK**, repair share 40% (17 of 42, the same as on 0.64.15 + F: Zeke's patch doesn't move it). cadet_test against 0.64.16: DIFFERENCES FOUND, the same as on 0.64.15; with the section 14/16 code (and build lines) put back: **ALL IDENTICAL** to 0.64.16. **F stays PASS on 0.64.17.** SC1's own full round on 8d65f86f (15:04 UTC): all OK (check_fast, player, food 11 4 and 1 7, intro --week, interactions, day_check 0 1 5 7 12 13 16 19 21 27, events, fridays).

**mech_check m12 fix: claude/patch-play1-f 5640cf5a, PASS** (16:15 UTC, lead 28; CR6's full-round FAIL on 0.64.17: "m12: the flagged machine seen to by the night crew at 22:00", night ['open', None]). Cause, confirmed: M12 replays the machines to Day 12 16:30 and plants its own jobs on Washers 1-3. On 0.64.17 the replay has already posted a real open Washer 3 service job (`4-washer-3@273`, Day 12 09:00; the moved mornings wear it a little sooner), and on 0.64.16 there is none (my probe on both builds). The logbook and the 22:00 night crew rightly take the real job, so the planted one stays open: a check fixture clash, not a game fault. The fix is in mech_check.py only (one line, M12's setup: drop jobs on Washers 1-3 before planting the shift); the game file is unchanged from dd83d896. My runs with the fixed check: mech_check (all parts) on the 0.64.17 candidate 1d2f3269 **MECH CHECK OK**; m12 on 0.64.16 b9f053ba **OK**. The morning and night-shift checks and cadet_test stand as above (same game). A check change: the check was wrong (it assumed nothing else touched those washers), so the owner's review is this one (24n is the Works career engineer's seat).

**Line supper fix: commit 599de448, tip claude/patch-play1-f 7f07d035, PASS** (16:45 UTC, leads 28/29; CR6's bigevents_check FAIL on the 0.64.17 candidate: silva-bea ate standing at the Line supper; 0.64.16 OK). 7f07d035 = 5640cf5a + 599de448 + a merge of integration-next 8193458e (whose game is the 0.64.17 candidate's, sha256 22583691...). Cause (SC1's, consistent with the code): a meal tradition's set-off is a fixed allowance, but tradMeal's walk to the servery line depends on where they are; from the garden's far beds (3-tend-16) the walk took 26 of her 31 minutes, leaving 14 to sit, under the least time seated (20). Fix, section 14's tradMeal only (two lines): when the walk would leave less than the least time seated, the previous segment ends that much earlier (at most half of it; never a commute, a stop or an event meeting), as take()'s WALK_LEAD does. General, not special-cased; no R().
Breadth: the crew's plans for every person, Days 1-28, as shipped: **0 of 4,116 person-days changed** (the Line is placed on its day only in bigevents_check's calendar copy), so the game as played is unchanged now; the rule applies whenever a meal tradition meets a long walk.
My runs on 7f07d035: bigevents_check **OK** (the Line supper: 83 mean to go, 71 came, at most 44 at once, 48 seats); events_check **OK**; cadet_test against the candidate 8193458e **ALL IDENTICAL**; check_fast **OK** (364 s); food_check 1 7 **OK**; day_check 7 **OK**; mech_check **OK**.

Notes (no change needed):
- brennan.lines:124 "Dinner's till eight" (dinner runs to 20:30): pre-existing, left; a backlog row if wanted.
- The build-table row says the branch is from 32b699a6 and has no cadet_test line: BM13 may want to add "cadet_test: crew mornings moved; schedule code reverted = ALL IDENTICAL" and the 40% when merging.

## Summary (06:15 UTC)

| Part | Tip | Verdict |
| --- | --- | --- |
| B, notes 9-12 (FR4) | claude/patch-play1-b 4d062c45 | PASS |
| J, note 20 (CK1) | claude/patch-play1-j ec06f68e, then 4bc3e39c | PASS (after one fix asked at 1188cbdf); the toast-gap fix 4bc3e39c PASS |
| E, notes 14, 16 (LD1) | claude/patch-play1-e 7e26050e | PASS (e36549af had no game change) |
| F, note 18 (SC1) | claude/patch-play1-f dd83d896 | PASS; re-checked merged as 0.64.17 1d2f3269: PASS |

