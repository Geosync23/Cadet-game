# Handover: reviewer PR8 (second Fridays reviewer)

Written 2026-10-21 by PR8 (session_01Nrvf1SYaXHTLwssGoBfJ54) before the account move (lead 24's ask). Read
`plans/review-8.md` first: every result, find and verdict is there.

## Role, branch, people

- **Role:** second reviewer for Short Fridays, beside PR5 (session_01Eh4drBZjJ82DjYx6XaTt1F, turns 7, 8, 9, 11b2220).
  PR8 takes FR3's turn 10 (the switch on) and FR3's fix turns.
- **Branch:** `claude/review-8` (from claude/fridays 0dc4562). Push only there; the game is never changed here.
- **Lead:** lead 24, session_01SDe7z5Nr7u69uH1k4sjZ8r. **Builder:** FR3, session_01935gmiyLoy5fgvs3xQd7QC.
- Verdicts go to FR3 and the lead by send_message.

## State

| Commit | What | Verdict |
| --- | --- | --- |
| 0dc4562 | Turn 10: SHORT_FRIDAY on; Day 19's Sunday lines, `{sunleavers}` | PASS WITH FIXES (sent) |
| 208581c | PR5's turn-6 fixes: friMissed + SIM_ADVANCE hook; player_check TOK; fridays_check cases | PASS WITH FIXES, provisional (player_check not run) |
| e18844f | Backlog #20 (section 14: an alts-only intro beat holds its first alt); fridays_check storm stubs | no verdict: only cadet_test (ALL IDENTICAL) run |
| (to come) | FR3's `arriving` fix for Day 19's welcome line | not reviewed |

Open fixes for FR3: the old-save Friday-evening dip (find 3); Day 19's welcome (FR3's `arriving`). Release rule:
Fridays + EVENTS_ON + EV4's storm update together, or Day 12 is a silent hall.

## Left to run (stopped by lead 24, 2026-10-21 ~17:52)

1. 208581c: `player_check.py` with the switch on (~30 min): the job loop should skip 7-aud-seats and pass.
2. 208581c: `mutants.py m11_nohook m12_mailnow` (both should be CAUGHT; ~20 min).
3. e18844f: intro_check `--week` on and off (d5-mug heard 3 of 3), `--firsts`, `--evening`; day_check 1 and 5.
4. FR3's `arriving` fix for Day 19 (when pushed), and FR3's fix for the old-save Friday dip (find 3).
5. Not done in turn 10's round (FR3 ran them): bubble, interactions, clothes, talk, social, intro, devmode, career,
   mech, puzzle, food, perf, arc, path, tiles, disc. The Day 12 probe on the EVENTS_ON copy and Day 19's live probe.

## How to test (what PR8 did)

- Setup: `pip install playwright`; three@0.128.0 and acorn@8.12.1 under /tmp/cadet-work (DEV_NOTES "Testing").
- Copies: `sed 's/^const SHORT_FRIDAY = true; /const SHORT_FRIDAY = false;/'` (note the space: the pushed line is
  `= true; ` padded); `sed 's/^const EVENTS_ON = false;/const EVENTS_ON = true; /'`.
- `plans/review-8/runner.sh 'name:cmd' ...`: resumable (res/<name>.done); `$B` = the copies' folder, `$H` = the
  worktree. One check at a time on 4 cores.
- `plans/review-8/p8_fri.py BUILD TAG d5|up|d12|skip [DAY MIN]`: the live probe at 390x844 on a real save.
  `d5` from 15:12 takes ~50 min (the mess stretch is slow and stands at Deck 3's lift, not the mess: fix its goToDeck
  spot before relying on it); `up` ~5 min; `d12` ~20 min; `skip` under a minute.
- `plans/review-8/mutants.py [names]`: mutants in 208581c's build against its fridays_check (~10 min each).

## Gotchas

- `pkill -f <pattern>` kills your own shell when the pattern is in its command line (exit 144). Kill by pid.
- Background commands stop at their 2-hour limit and at the account's usage limit: the runner is resumable, so
  rerun the same list (a step killed mid-run may be marked done: check its log's rc line).
- events_check and bigevents_check on an EVENTS_ON-flipped copy fail on the events base's own parts (bigevents flips
  the switches itself); compare against the control copy (EVENTS_ON on, Fridays off).
- A probe that reuses a tag overwrites `shots/<tag>_res.json`; the logs (res/p_*.log, copied to plans/review-8/) keep
  each run.
