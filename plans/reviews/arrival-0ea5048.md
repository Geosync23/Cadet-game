# Review: claude/arrival 8c28e91..0ea5048 (0.42.20-0.42.21: Zeke's guided tour, the dinner meeting, the first-night bed arrow)

Reviewer 1c, 2026-10-17. Diff: `git diff 8c28e91 0ea5048` (section 21, intro_check part 7-8 and 10, DEV_NOTES, two screenshots). Tested on a scratch merge **arrival 0ea5048 + sim bfcd864 + content a6dd44c** (the only conflicts were the build lines and one DEV_NOTES row).

**Verdict: PASS WITH FIXES.** Safe to combine: nothing regresses, and intro_check is OK on the merge. But the tour, the user's main ask here, mostly doesn't reach a player who follows Torres. That one is HIGH: fix it before the user plays it.

## Checks
- **intro_check on arrival + sim + content: OK** (all 11 parts; the real walk misses nothing; draw-call peaks 190 / 206 / 289). Part 8's per-place count matches the writers' exactly (5-9 lines a place, 61 in all). One run timed out loading part 9's page while I had a second browser running; it passed when run alone.
- `introDinner` is in the step order (servery > table > chief), its fallback chain is right, `introSeat` seats you from `table` on, and the stand-in script has a choice.
- `introWriterLine` now picks the exact flagged line and fills it with `linesFill`. That's correct, and the counts prove it.
- **The bed arrow works:** in the real walk, at 19:05 on Day 0 the goal is "Your bunk" (`done.bed` unset, `INTRO_UI.bed` true). The tour's bunk stop doesn't count as finding the bed: the checkpoint [8,3] is 2 tiles from the berth's place [8,1], and the limit is 1.5.

## HIGH: following Torres, you hear 19 of the tour's 61 lines, and 4 of 10 places say nothing
I hooked `bubbleSay` in intro_check's own part-8 follower (one tile every 20 frames, 2 tiles behind Torres, on the merge above) and logged each place as it triggered and each line as it was said:

| Place | Triggered | Heard / written |
| --- | --- | --- |
| shuttle | 17:40, **the same tick as bay** (start tile [8,8] is in both ranges) | **0 / 5** |
| bay | 17:40 | 1 / 5 |
| haulway | 17:42, **the same tick as stores** ([12,8] is in both) | **0 / 6** |
| stores | 17:42 | 1 / 5 |
| lift | 17:44 at [13,7], **before works** (lift's range reaches the path to Works) | **0 / 5** |
| works | 17:45 | 1 / 9 |
| officers | 17:48 | 2 / 6 |
| wing | 17:52 | 3 / 6 |
| deck3 | 17:59 | 5 / 8 (you wait for the lift there) |
| servery | 18:11 | 6 / 6, but see the next finding |

Three causes:
1. **Several places can trigger on one tick.** The `for` loop in `introTourTick` sets `INTRO_UI.lines` for every place in range, so the last one wins and the earlier one is never heard (shuttle, haulway).
2. **Places can trigger out of order.** Lift fires on the way to Works, so its lines are cut off by Works, and nothing is said when you actually reach the lift.
3. **The pacing can't fit.** 5-9 lines at 3.6 s each is 18-32 s a place, about 4 real minutes for the tour, but Torres walks it in about 1 real minute and the next place drops the rest. "Stand still to hear a place out" doesn't help: he walks on and calls you.

I tried two quick patches on a copy (one place per tick in tour order; keep one line of the last place). Neither gets past about 1-2 lines a place on Deck 5, because cause 3 decides it. So the fix is a pacing decision for the onboarding seat (with the sim engineer if Torres's walk changes):
- **Must, whatever else:** trigger at most one place per tick, the first not-yet-done place in `INTRO_TOUR` order; a later place triggering marks the earlier ones passed. Also shrink or move the radii so no two places overlap on the walking line (shuttle/bay, haulway/stores, stores/lift on Deck 5).
- **Then either** Torres lingers at each tour place while its lines play and you're within about 3 tiles (the escort's lead waits on `INTRO_UI.lines.length`, with a cap of about 20 s a place so a player who runs ahead isn't held up). That's the closest to the user's "a proper introduction the whole way".
- **Or** each place plays 2 lines while walking (the writers mark which), and the rest go into `walk.more` for when you stand with him.
- **intro_check:** add the `bubbleSay` hook to part 8's follower and fail if any place is heard fewer than 2 times (today it counts what's written, not what's said). My probe: `plans/reviews/arrival-0ea5048-tour_probe.py` (run it from a checkout).

## MEDIUM: a place's leftover lines play over the dinner and the Chief
In the same run the servery's queue was still playing at the table: "That's Chef Brennan. Thank her on the way past." at 18:13, then "Soup's fine…", "Sunday's bread day…" and, at 18:25, **"I'll find us a table. Window side, if it's free."** That came after you've sat with him, had the dinner chat and met the Chief. The tour only waits while `DIALOGUE` is open, so its lines fill the gaps between the meetings.
**Fix:** when the step becomes a meeting step that isn't on the walk (`table`, `chief`), drop `INTRO_UI.lines` (the servery's last lines are about getting a tray and a table, so they're stale by then); or play the place's lines only while the step is that place's walking step.

## Low
- His calls (`walk.call.*` through `introSay`) and tour lines share one bubble with no gap check: at 18:07 one line showed for 0.23 s before the next replaced it. Have calls respect `INTRO_UI.next`, or push them to the front of `INTRO_UI.lines`.
- `I.done['tour:<id>']` goes into the saved intro state, but `INTRO_UI.lines` doesn't. A reload mid-place loses that place's rest. That's fine; it just shouldn't count as heard in any check.
