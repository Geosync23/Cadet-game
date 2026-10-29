# 0.98.0 full round: runner R1 (AS1)

- NEW: `claude/staging-pad` 7a2ae7d2, game sha256 `22f8939dbfea2dcf4b994dd8bfd7c8868f9d5450dd73c680c1dfd3c19d11918f` (matched).
- OLD: 0.97.0 610ad7f1, game sha256 `0bd1b5b69d640c7d2bd82032f2258e5be944f7905541dada62f9e4e9e615b36f` (matched).
- BM20's GO 07:38 UTC 2026-10-29; checks from 7a2ae7d2; two browsers, each its own CADET_WORK.

| Check | Result | Key lines |
|---|---|---|
| arrows_check step6 teachoff | OK | ARROWS CHECK OK |
| arrows_check step6 asis / track / skiptea | **FAIL (NEW)** x3 | "sleep by day: its level-1 arrow (p5n:bed:22) never led" (OLD OK; reproduced) |
| arrows_check step5 | OK | ARROWS CHECK OK |
| arrows_check endstay | OK | ARROWS CHECK OK |
| arrows_check (default parts) | OK | ARROWS CHECK OK |
| arrows_pointer_check | OK | arrows_pointer_check: OK |
| player_check (with the night part) | OK | PLAYER CHECK OK |
| bubble_check | OK | BUBBLE CHECK OK |
| puzzle_check | **FAIL (NEW)** | "p6's first: the save round trip mid-case (3514 bytes)" (budget 2600; OLD 1924; reproduced) |
| social_check | OK | SOCIAL CHECK OK |
| talk_check | OK | TALK CHECK OK |
| day_check 4 | OK | DAY CHECK OK |
| day_check 11 | OK | DAY CHECK OK |

## step6: a game gap in 28a (S6-1, the nights)

On Day 22 a player who doesn't clock in that morning never gets the day-sleep arrow. Trace on NEW (asis): after the
Tier 4 test the follower takes a board job (09:50); "Clock in: shift at 09:00" is a level 4 arrow, not followed. At
12:30 `yourShift(22)` becomes `{"day":null,"night":[1365,1800]}`, and p5nGuide's `S && S.day && m >= S.day[1] &&
p5nDayBed(now)` is false, so neither p5n:dayout nor p5n:bed is asked, although `p5nDayBed()` is 1005 (sleep until
16:45). OLD passed by luck: a level-1 arrow was due at 09:51, so the follower clocked in on the way, then clocked out at
12:30 and went to bed at 12:31. A real player who skips clocking in on test day would never be told to sleep before
their first night. Fix idea for 28a's owner: when S.day is null but p5nDayBed(now), still ask p5n:bed.

## puzzle_check: the p6 save budget

The p6 case is identical on OLD and NEW; the save round trip reads back the same (saveSame). But on NEW
`SHIP.works.cases.open` holds two cases at that moment (`creserve39:3-recycler-1@32010` and `c3-filter-1@536`; OLD:
only the first), so the saved cases are 3514 bytes against the check's 2600. A check budget that assumes one open case;
the owner's call (24k / puzzle_check), with a look at why a second case is open there now.

**R1: two NEW FAILs (one game gap in 28a, one check budget), the other 13 OK.**
