# Handover: RC (rec engineer, the 0.64.1 determinism fix) — PAUSED by the user

- **Role:** RC, started by lead 19 to fix BM9's find on the 0.64.0 candidate (`claude/rec-cand-s1` 50d55ef): machine_check
  failed determinism with REC_DECK = true ("wear differs (caches cleared)", traced faults "the same twice False").
- **Branch:** `claude/rc-wip` (WIP, on 50d55ef). NOT yet on `claude/rec-cand-s1`; BM9 has since pushed check-only commits
  there (6e20c89 device_check, then a disc_check line): rebase onto them before moving this across. Never force-push.
- **Build:** 0.64.1 in the HUD and GAME_BUILD. No DEV_NOTES row yet (add one when it lands).

## Cause
recVisit (RA's crew planning) asked RB2's `recShutAt(B + t + C)`, which reads MACH_HIST and falls back to the latest
recorded hour for the future, so a day's plan depended on when it was planned; and the plan cache (SHIP_DAYS) kept plans
made against an earlier machine history across machinesReset (the traced-faults run reused the previous run's plans).

## The fix (in the diff, all marked "RC, 0.64.1")
- `recPlanShut(d, occ)` (beside recShut): the plan for day d reads the record at 22:00 the evening before
  (hour `(d - 1) * 24 - 2`), only once it's settled (`recSettled(h)`: `h <= MACH_HOUR - 2` and recorded; a repair rewrites
  the hour before the one running). Not settled yet: all clear (REC_OK), and `occ.recAt` / `occ.recSet` mark the plan.
- recVisit calls `recPlanShut(d, occ)` instead of `recShutAt(B + t + C)`.
- shipDay: a cached plan made before its rec hour was settled is planned again once it is.
- machUseDay: doesn't keep (MACH_USE) the use of such a provisional plan.
- machinesReset: drops cached plans (and their MACH_USE) that read the old record.
- REC_DECK = false: recPlanShut returns REC_OK without marking anything, so nothing changes.
- Tried and rejected: the record two days back (`(d - 2) * 24 - 2`): deterministic, but avoidance almost never bites and
  the steady player goes to 6.1 jobs a shift day (same as no avoidance). The evening-before hour gives 5.7 (as 0.64.0).

## Checks so far (each with its own CADET_WORK; /tmp/rc/runone.sh style)
- machine_check, switched on: **OK** (same twice / one jump / odd minutes / caches cleared all True; traced faults the
  same twice True; steady player 5.7 a shift day, bands unchanged).
- machine_check, REC_DECK = false: **OK**.
- deck_check (on): **OK**.
- cadet_test 0.63.5 final be3d7ee vs this build with REC_DECK = false: every screenshot 0 px different, but
  "DIFF state ['items']" — **the same on the untouched 0.64.0 with REC_DECK = false**, so it's from the 0.64.0 merge, not
  this fix (not yet looked into what the items difference is).
- events_check (on): FAILED only on 'dayReport work: volkov-maeve 476/480' — **the same on the untouched 0.64.0**.
- day_check days 1 and 2 (on): only FAIL is 'work: volkov-maeve 476/480' (pre-existing, lead's item A below). Days 3-8
  not run (paused).

## Left to do
1. day_check days 3-8 on.
2. Lead's item A: Maeve's rec round (recRound) lift rides (~10:26-10:28 down, ~10:58-11:00 back) are act 'commute'
   mid-shift, so dayReport counts 476/480 work. Fix the planning side (the round's rides count as on-shift), not the check.
3. Lead's item B: career_check 'busy: Relied on before Day 5' with the deck on (43 xp by Day 4 vs 37 off). Recheck after
   the fix; if still failing, lead's call: rec deck machine jobs give half career xp, one named constant, no band change.
4. Move onto `claude/rec-cand-s1` (rebase onto BM9's commits), DEV_NOTES row, push, send the hash and results to
   lead 19 (session_01FsGspstkG61e9AWadSi36y), BM9 (session_01W4FMKvz4gV1LWn5jnLaQVT) and R7 (session_01HCwvy5w432bhz41UYxHYwq).

## Gotchas
- The route in recShutAt reads the holds' *current* lastService, not the recorded one, so a route could differ if the
  holds are serviced between the 22:00 record and the planning (rare; RB2's function, left as is).
- MACH_HIST isn't saved: after a load, days whose 22:00 hour is before the load plan with all clear (as before, the old
  fallback wasn't reload-stable either).
- MACH_NORM's days 1-7 are planned early, before their hours are settled, so they see all clear (deterministic).
