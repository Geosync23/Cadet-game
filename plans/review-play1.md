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

**Verdict: PASS WITH ONE FIX** (one guarded line in J's clockRemindTick; then no re-review needed beyond a look at the line and check_fast).

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

## E. Ladder taps and the rower (notes 14, 16), LD1: claude/patch-play1-e

(waiting for the tip)

## F. Breakfast at 07:00 (note 18), SC1: claude/patch-play1-f

(waiting for the tip)
