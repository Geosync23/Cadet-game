# Round "fable", share R4 (session_01GKuymnZfZ6qmpeytQExvGQ), 2026-11-15

Candidate 1: claude/staging-fable-review c4999dae, game sha256
d6b9ce81a5254ab089f07afad01ed20edbd05e38d12a6043092f0578f9efa1c0 (matches; label 0.99.92-review).
OLD (only where named): 0.99.91, main cdd9efd, game b321a4ec...95f3 (checked).
Each check ran once on the candidate, two lanes side by side (two browsers at most). Not run here, by the round's
rule: robust_check and device_check (BM29's wave 1 runs on this exact file are the round's runs).

**Result: R4 OK, with one one-off to note (title_check) and one observation for FR2 (fresh_walk, Day 2 18:00).**

| Check | Result | Key lines |
|---|---|---|
| career_check | OK | exit 0, `CAREER CHECK OK`, 178 s, skipped 0 |
| appt_check | OK | exit 0, `APPT CHECK OK`, 743 s, 223 ok lines, skipped 0. The 4 FAIL lines in its log are its own self-test (planted faults: "planted: ... its part fails" ok) |
| saves_check | OK | exit 0, `SAVES CHECK OK`, 230 s, skipped 0 |
| title_check | OK on 3 runs of 4 (see below) | first run: stopped, exit 1, after 33 ok lines; reruns 61 ok, 0 FAIL, `TITLE CHECK OK` three times; OLD the same once |
| day_check 6 | OK | exit 0, `DAY CHECK OK`, 277 s, errors [], skipped 0 |
| day_check 8 | OK | exit 0, `DAY CHECK OK`, 294 s, errors [], skipped 0 |
| day_check 23 | OK | exit 0, `DAY CHECK OK`, 286 s, errors [], skipped 0 |
| day_check 24 | OK | exit 0, `DAY CHECK OK`, 277 s, errors [], skipped 0 |
| day_check 16 | OK | exit 0, `DAY CHECK OK`, 285 s, errors [], skipped 0 |
| fixtap_probe (copy with FIXTAP_ON false) | OK | exit 0, `FIX TAP PROBE OK`, no page errors, skipped 0 |
| rv31 fixtap_reach BUILD | OK | exit 0, 311 rows, `page errors []` (no OK line by design), skipped 0 |
| rv31 fixtap_click OFF BUILD | OK | exit 0, off and on `errors []` (no OK line by design), skipped 0 |
| cr1_check | OK | exit 0, `CR1 CHECK OK`, 14 s, skipped 0 |
| p926_check | OK | exit 0, `P926 CHECK OK`, 559 s, 65 ok lines, skipped 0 |
| rv32 fresh_walk BUILD 3 | OK by its five points (see the observation) | exit 0, `long []`, `stuck []`, `errors []`, 341 s, skipped 0. Record: plans/fw-fable-r4.json (OLD: plans/fw-fable-old-r4.json) |

"Skipped" lines: 0 in every log.

## title_check: one stop in four runs (a timing one-off; not a FAIL line)
- Run 1 (in lane B, one other browser running): 33 ok lines, then a crash, not a FAIL: title_check.py line 176, the
  second pass of "Start over for a player who has arrived before" (the 'Arrive by shuttle' choice), right after
  "Skip to Monday morning: the terminal goes onto Monday 06:00". `pg.click('#tiNew')` then `pg.click('#tiOver')`
  timed out after 30 s: the START OVER button was there but not visible.
- Reruns on the candidate: three, each 61 ok, 0 FAIL, exit 0, `TITLE CHECK OK` (one beside the OLD run, two side by side).
- OLD (0.99.91): 61 ok, exit 0, `TITLE CHECK OK`.
- Read: the check's own timing (a click on New game that did not open the question once under load), not seen again in
  three tries. Suggest a backlog row for the check (wait for #tiAsk to show before clicking #tiOver at line 176).
  BM29 and lead 52 were told at once.

## fresh_walk: the five points, and one observation
1. Day 1's briefing meets and the Chief stays to its end: arrow "Morning briefing with the Chief, 08:50: the Works
   bay" walked to at 08:20; the talk read on from 08:50 to 08:53 (reply "Ready when you are.").
2. Day 1's arrow leads to the Works bay before 08:50, then to the clock: 08:53 "Clock in at the time clock", clocked in.
3. Day 2's 08:45 meeting: arrow "The Chief's office, 08:45: your first solo job" from 08:31, the talk 08:45 to 08:46,
   "Your first solo job" at 08:46.
4. Day 2's 18:00 booths: arrow "Calling home, the booths on Deck 3: Leila shows you how" walked to at 18:00, shown to
   18:16 (the same minutes as on OLD and as in round 0999's record).
5. No page errors; the follower never stuck an hour; `long []`.

**Observation (new against OLD, for FR2 / BM29 to judge; not a failed point):** Day 2 18:00 to 18:12, at the booths.
- OLD: the follower's tap on the floor at the arrow's pin sits you down ("Call-home booths: You sit down").
- Candidate: the same tap, five times (18:00, 18:03, 18:06, 18:09, 18:12), is each followed by "close the chat with
  Davi Keane": a person's card opens instead, and you never sit in the booth. This is the opposite of what FRP_PINTAP_ON
  is meant to do (a tap at the pin with someone standing there does the arrow's thing, not their card).
- The two walks already differ earlier that day, as expected: on OLD a "Missing people" arrow at 12:27 sent the walker
  to call home at lunch; on the candidate that arrow did not come (the needs arrows changed with FRP_FOOD_ON), so at
  18:00 the candidate's walker had not called home and "Missing people" fired at 18:10. So who stands at the booths
  may differ too. Not looked into further (cost); the two records are in plans/ for whoever does.

## Kit (this container)
Candidate in /home/user/Cadet-game; OLD worktree /tmp/old-fable; CADET_WORKs /tmp/work-r4, /tmp/work-r4b; three r128 and
acorn in /tmp/cadet-work. fresh_walk on OLD: run from the OLD worktree with the candidate's copy of the probe.
