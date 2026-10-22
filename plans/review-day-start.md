# Review: "Start at Day N" on the Dev page (DS1), claude/day-start 64583ba1 (RV6)

Reviewer RV6 (session_018Jzc4LeoHvuahsS7VHAzn3), 2026-10-22, for lead 28. Builder DS1 (session_01MZBSf7MZeb9C89wpoavLko).
What: section 25 only (Dev link only): `DM_DAYS` (8 recorded saves, 170,459 characters on one line), `devmodeDaySum`,
`devmodeDayUnpack`, `devmodeStartDay`, `devmodeDaysRow`, and one call line in `devmodeSet`; `tools/day_saves.py` (the
recorder); `devmode_check.py` part "days".

## Verdict: FIXES NEEDED (item 1 in the recordings, item 2 in the recorder's setup)

## What was run
| Check | Result |
|---|---|
| cadet_test 2b4a05db vs 64583ba1, alone (no #dev) | ALL IDENTICAL |
| check_fast on 64583ba1 | QUICK CHECK OK in 252 s |
| devmode_check days (clean) | DEVMODE CHECK OK |
| Planted faults, devmode_check days (6) | 6 of 6 caught: a wrong day, no Undo, the real save written, the DecompressionStream test removed, tracking off, the busy flag left on after a damaged record |
| day_saves.py --twice (with ARROWS_CHECK from claude/arrows-plan 14cffba, item 2) | DAY SAVES TWICE OK; both recordings match the build's Days 1-2 sizes exactly (11,660 and 13,624 packed). Day 1 is played; the follower fell behind on Day 1 (never clocked in), so Days 2-8 are Set career, as the brief expected |
| Load outside Dev, 5 loads each, with and without the block | heap +0.6 MB (89.2 vs 88.6 MB median); load median 6.41 s vs 6.01 s (noisy: one load of five was faster with the block); file +167 KB (5,826 vs 5,659 KB) |

Plant runner and logs: `plans/review-day-start/` (plant.py, p_load.py, the logs).

## Numbered list

1. **The Set-career stand-ins (Days 2-8) start a day ahead (must fix).** For each day the follower couldn't reach, the
   recorder calls `devmodeSetCareerTo(d + 1)` for the Day d+1 06:00 save. That sets the career *through* that day, so
   at 06:00 the day's own lessons are already learned. From the recorded summaries: Day 2 06:00 has m1 (Rounds, taught
   that day at 10:45) trained; Day 3 has m4 and m3d; Day 4 has m5 and m3i; Day 5 m7 and p3; Day 8 m6 and m2. A tester
   who picks "Day 3" to try Hauling finds it done. (arrows_check's `real_game` uses `devmodeSetCareerTo(day - 1)` and
   then skips to the morning for the same reason.) Fix: `devmodeSetCareerTo(d)` then skip to Day d+1 06:00 in bed (as
   arrows_check does), re-record, and add a check line: no lesson of Day N's (arrows_check's WEEK) is trained at Day N's
   start.
2. **day_saves.py can't run on its own branch (must fix or decide).** It needs `arrows_check.py` (its follower), which
   is on claude/arrows-plan, not on claude/day-start or integration 2b4a05db. On the branch as reviewed it stops with
   "needs arrows_check.py"; I ran it with ARROWS_CHECK set to the arrows branch's copy (14cffba). Either merge after
   the arrows check lands in integration (say so in the build table) or carry a copy.
3. **The work log is empty on every recorded day (lead to decide).** `jobs: 0` on Days 1-8 (the summaries), while the
   band climbs to "relied": Set career sets the band but leaves no Work log. A day started here looks like a player who
   never turned a job in. Fine for testing lessons; worth saying on the Dev page, or recording through play once
   FX1-FX3 land (as planned).
4. **The block costs a little outside Dev (small).** `DM_DAYS` is a top-level constant, so every player's load parses it
   and keeps it: about +0.6 MB of memory and +167 KB of file (about 3%); load time was within noise on my runs. If
   that matters on phones, keep the text in a non-script tag (`<script type="application/json">`, read only in Dev).
5. **Upkeep (note for DEV_NOTES).** devmode_check's days part compares each start with its recording, so any change to
   the career, jobs, Mail or the save's shape makes it FAIL until someone re-records (about 15-20 minutes, and the
   block's 170k line rides into that commit). DEV_NOTES says when to re-record; the build master should know this
   check will go red on career changes and what the fix is.

## Checked and fine
- Without `#dev`: nothing runs (the row is drawn only by devmodeSet); cadet_test identical.
- A start writes only the Dev keys (`starship-cadet-save-dev`, the arrived key with `-dev`), keeps an Undo first,
  refuses while busy, refuses a damaged record and a browser without DecompressionStream with a message and the Dev
  game unchanged; the planted faults above show the check notices each.
- Each start lands at Day N 06:00 beside your bed with tracking on (the check's lines, all passing).
