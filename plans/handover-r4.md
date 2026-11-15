# Handover: check runner R4 (session_01GKuymnZfZ6qmpeytQExvGQ), 2026-11-15

Role: check runner R4, round "fable" (0.99.92-review, claude/staging-fable-review c4999dae, game d6b9ce81...a1c0).
BM29 gave the FINAL GO; stood down on BM29's word. Older notes: plans/handover-r4.md on claude/checks-09991-r4 and
claude/checks-0999-r4 (same setup).

Branch: **claude/checks-fable-r4** (from c4999dae): plans/checks-fable-r4.md (results and the follow-up walks), the
fresh_walk records plans/fw-fable-r4.json, -run2, -fr1off and fw-fable-old-r4.json, and this note.

## The share this round
career, appt, saves, title_check, day_check 6, 8, 23, 24, 16, fixtap_probe (copy with FIXTAP_ON false), rv31 fixtap_reach
BUILD, fixtap_click OFF BUILD, cr1, p926, rv32 fresh_walk BUILD 3. (robust_check and device_check were BM29's wave 1.)
Two lanes, about 25 minutes: lane A the five days then fresh_walk; lane B the rest in that order.

## Setup (fresh container, about 2 minutes)
`pip install playwright numpy pillow` (never `playwright install`); three@0.128.0 and acorn@8.12.1 by npm pack into
/tmp/cadet-work/{three,acorn}; one CADET_WORK per lane (/tmp/work-r4, /tmp/work-r4b: a test/ folder and symlinks to three
and acorn); CADET_CHROME=/opt/pw-browsers/chromium. The probes are in the repo now (plans/rv31-probes, plans/rv32-probes).
OLD: `git worktree add --detach /tmp/old-XXXX <commit>`; to walk OLD, run the candidate's copy of fresh_walk.py from
inside the OLD worktree (it reads arrows_check.py from the folder you are in).

## Gotchas
- title_check stopped once in four runs under load: line 176, click on #tiOver timed out (button not visible) in the
  "arrived before, Start over" part. Three reruns and OLD passed. The check's own timing; a backlog row was suggested.
- appt_check's log holds 4 FAIL lines from its own planted-fault self-test; the pass is exit 0 and APPT CHECK OK.
- fixtap_reach and fixtap_click have no OK line: pass = exit 0 and "page errors []" / "errors []".
- fresh_walk repeats itself except for a few minutes' drift under load (same arrows; Day 1 evening lines 7 to 14 minutes
  apart when another check shared the machine). Compare records with a first-difference script per list (acts, arrows,
  toasts, tips), not by eye.
- From 0.99.92-review the walk differs from 0.99.91 from Day 0 18:26 ("A seat for your tray"); on Day 2 18:00 the pin
  taps at the call booths open Davi Keane's card (closed as old by RV37 and FR2). The next round's OLD record is
  plans/fw-fable-r4.json.

## Loose ends
None.
