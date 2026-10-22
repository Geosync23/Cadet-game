# Handover: FX2 (Pillar 5 fixes, part 2, then fresh-eyes fixes)

Session: session_01JRCSTi6r1qQ51mTgwgJ7es. Branch: `claude/p5-fix2` (the only branch this session can push to). Lead: lead 29 (session_01A9rNreAGVbsY1HgPucDMA7). Written at about 55% memory, at lead 29's request; idle after this.

## What's on the branch, in order (all pushed, all reviewed and passed)

Started from claude/integration 2b4a05db (0.64.15).

| Commit | What | Reviewer |
|---|---|---|
| e10d81a | A. The fire drill (M3, Day 3) can be done by taps: 15b's `ixSides()`/`ixChores()` let a side job's stop take a tap, the arrow moves stop to stop and clears (`drillGoal`), the Calendar names the Works bay | AR2 PASS |
| 03f9eb9 | B. Scanner training (M7, Day 5): `scanFirst`, the look-over is the scan and shows P3's case; section 15's `jobEnd` asks 24k's `caseFitted` before a panel repair finishes (before, any repair in real play settled every head-scratcher and scanner pick); `WORK_MECH[id].counts` / `worksCounts` in 24 core (m7: only a scanned job trains you) | AR2 PASS |
| 1ae2d27 | C. Wording: Tuning and Hauling asks use `{time}` / `{place}` (content/works/works.lines, re-baked); a tune job's arrow says "Tune the"; the Calendar's inspection is 06:30 (`inspectCalendar`) | AR2 PASS |
| a76ec6c | A1. No drill taps before Calder's call at 14:50 (`ixSides` waits for `j.found`) | AR2 PASS |
| a3b93ce | B widened: the user's scan-first rule on every faulty-machine job once you have the scanner (design-doc Pillar 5 Tools line); `scanFitted` counts the job's own part as your pick (the scanner use counts when you follow the arrow); `worksWatching(j)` keeps the teacher's watch job off your board (all trainings); 24k's clue toast had one argument ("undefined") | AR2 PASS |
| cc2bb2b | mech_check: watch-job lines for m4 and m5 too | AR2 PASS |
| 507af1a | merge of claude/integration b9f053ba (0.64.16) | |
| 191d185 | Eating (fresh-eyes item 17): a tray is eaten at any seat you sit on, not only `mess-seat` (the long table and lounge seats only sat you) | AR2 PASS |
| 31477c3 | merge of claude/arrows-c 6610dc7 (base for fresh-eyes batch 2) | |
| d59e8e9 | Batch 2, lead's item 29 / diary 36: a Clock in arrow you track on Day 1 stays up (Zeke's escort arrow no longer goes over it; his walk's end clears only his own arrow; the first-time arrows leave a goal with `trk` alone) | RV8 PASS |
| 493b84e | Batch 2, lead's item 40 / diary 48: any Tea corner chair gives you tea (`ixTeaAnywhere`: a free tea seat, else tea standing in the corner) | RV8 PASS |
| 421838e | player_check: the tea part puts the deck, clock and tea day back | RV8 PASS |
| ffdbb8c | RV8 on item 36: 15b's `trkDoneCheck` leaves a `clock:` goal alone (reaching the Works bay used to take it down) | RV8 PASS |

**Cherry-pick lists.** Pillar 5 fixes: e10d81a 03f9eb9 1ae2d27 a76ec6c a3b93ce cc2bb2b (these are already merged into claude/arrows-c). Fresh-eyes batch 1: 191d185. Fresh-eyes batch 2: d59e8e9 493b84e 421838e ffdbb8c (built on arrows-c 6610dc7).

## Checks added (each fails before its fix, passes after)
- mech_check: m3d "drill by taps" (plus a 14:20 tap starts nothing); m7 taps part (the teacher's watch job off the board for m7/m4/m5, clue toasts, an ordinary job scanned first with its use counted, the lesson by taps, no training without a scan); `fix2` part (asks' time and place, Tune arrow, Calendar 06:30). mech_check's and career_check's training players scan the m7 job first.
- player_check: "A tray at any seat"; the tea part (two then three tea places taken).
- intro_check: part 13b (`--firsts`), tracked Clock in on Day 1 through Deck 5 and the Works bay.

## Investigated, no code change
- Fresh-eyes item 23 (crew lying on the corridor floor): Esme asleep on a lower bunk in a see-through (cut-away) bunk room; the bunks fade, the people don't. The user chose to leave it.
- The Day 3 Hauling blocker: 15b ixBoard's `doable` gave hauls and rounds no Take it (AC2 fixed it in arrows-c 6610dc7). The next one, the laundry's folding table at the linen drop starting laundry instead of the drop, is FB1's (claude/fe-cartdock).

## Open points
- After the scan on a head-scratcher, the arrow says "Repair the <machine>" until you call it in Fault notes (a repair before the call now just says so). That pointer belongs to the arrows plan (piece C).
- Not reproduced from fresh-eyes item 17: the tray vanishing on getting up, and the lingering "You sit down" toast.
- A week rerun (arrows_check week, off and guide) is due once FB1's cart fix is on claude/arrows-c; last run on arrows-c 00f4436: Rounds learned on Day 2, Hauling stuck in 'do' from Day 3 (FB1's case).

## How I tested
Checks run in copies (git ls-files into a scratch folder) so the work tree can change meanwhile; never more than about 4 browsers at once on this 4-core machine (more gives Page.goto timeouts, not real failures). Probes drove the real game with Playwright: `Game(pw, path, w=390, h=844)` from cadet_test, `newGameStart(true)` + the name form for Day 0/1, `skipTo(introAbs(day, min))`, real taps through `playerTap` / `jobSpotTap` / `page.mouse.click` and `page.touchscreen.tap` (a page with has_touch).
