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

(in progress)

## E. Ladder taps and the rower (notes 14, 16), LD1: claude/patch-play1-e

(waiting for the tip)

## F. Breakfast at 07:00 (note 18), SC1: claude/patch-play1-f

(waiting for the tip)
