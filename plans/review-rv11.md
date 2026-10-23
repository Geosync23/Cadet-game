# RV11's reviews for 0.92.2 (2026-10-23)

Reviewer RV11, reporting to lead 31, then lead 32 (from ~20:30 UTC), and BM15. All three fixes are on claude/integration-next 54efee21 (the 0.92.1 candidate).
Runs: `plans/review-rv11/runs.txt` (each check's exit code, time and last line). Probes: `plans/review-rv11/*.py`.

| Fix | Branch, commit | Verdict |
|---|---|---|
| FX6 team repairs near new | claude/team-restore 28bcc102 | PASS |
| DV1 Day 2 solo job | claude/d2-solo-tap e81ef301 (292f4f77 + a test-only line) | PASS |
| FX3 relay shelf glow | claude/p5-fix3 04c38a76 (+ 5d1b7290 handover, docs) | PASS (after one fix) |
| DS1 goodnight words | claude/goodnight-words afc5e7a4 | FIXES NEEDED, then cancelled by lead 32 |

## FX6: TEAM_RESTORE 90 to 98
- One constant (section 17), used by the team finish and 24h's teamOthersRight. design-doc Machines paragraph added.
- machine_check: on 54efee21 it fails only on "team repairs leave machines at 90, not close to new". OK on the fix.
- mech_check: on 54efee21 it fails only on "m8: a team job leaves its machines close to new". OK on the fix.
- Planted faults, both caught by machine_check: TEAM_RESTORE 97 (the 98 line); the team finish left at 90 (5w, recycler 94.6 as it was done).
- check_fast OK; cadet_test ALL IDENTICAL; day_check 1 and 16 OK.
- What a player sees: machines fixed by a team job read 98% instead of 90%.

## DV1: a tap on the speaker walks you in; the arrow at the visitor spot
- introMeetGo (section 21) is asked first in introTap; the beat row carries `place: b.stand` (section 19).
- Part 18 (--solotap): fails on 54efee21 (arrow, walk, meeting); OK on the fix.
- Planted faults caught: no place (the arrow line); no playerGo (the walk and meeting lines).
- First gap: a wider time window was not caught. The 10:05 tap is refused by the met guard first.
- DV1 added an 08:35 tap (e81ef301). It catches the window start planted 30 minutes early (path 5), and passes on the fix.
- Full intro_check OK; interactions_check OK; check_fast OK; cadet_test ALL IDENTICAL.
- Side effect probed (d1_probe.py), the Monday briefing: a tap on Calder from the main lift at 08:52 walks you to the bay's first map tile [13,0], and the briefing starts at 08:55 as you enter.

## FX3: a tap on the glow takes the part
- First version (85b6250a) was on dbc62255, not 54efee21. It also asked the glow before tapCrew, so a tap on a crewmate standing in front of the glow fetched the part instead of talking to them. fx3_crew_probe.py: 30 of 30 fetch (54efee21: 30 of 30 talk).
- FX3 moved the glow tap to after tapCrew, rebased onto 54efee21 (04c38a76), and added a crew line to the check.
- FX3's block run alone (fx3_only.py): on 54efee21 the glow line fails (22 of 216); on the fix it passes (216 of 216), and the crew line passes (6 of 6 talk).
- Planted faults: glow before tapCrew (85b6250a's game) is caught by the crew line; the wrong shelf is caught by the glow line (216 of 216).
- My probe on the fix: 30 of 30 talk.
- Whole interactions_check, machine_check, player_check and check_fast OK.
- cadet_test: the first run showed 14,812 px in a_start, all inside a speech bubble, on a loaded machine. A re-run and a base-vs-base run were both ALL IDENTICAL.

## DS1 goodnight words (cancelled)
- "Breakfast from six", but the game serves breakfast from 07:00 (MEALS [420, 540]; the servery's text says 07:00).
- Lead 32 cancelled it: ZW1 misread MEALS.

## Gotchas
- interactions_check takes about 50 minutes with 3 or 4 browsers running at once; it is about 30 minutes alone.
- A copy of intro_check.py or interactions_check.py must keep its file name, because it finds cadet_test.py by replacing its own name.
- `pgrep -f`/`pkill -f` with the pattern in the same command line matches the shell itself; use `ps -eo pid,args | grep '[x]...'`.
