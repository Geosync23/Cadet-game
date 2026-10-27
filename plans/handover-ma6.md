# Handover: MA6 (mechanics seat A, Pillar 5 Step 6)

- **Role:** mechanics seat A for Step 6, hired by lead 41 (session_01GKuymjWR1dqfbCw1MyEP9j; send_message, priority "next"). My session: session_01GKuymj1UEDuEYMnG9rmFkc. Reviewer: RV23 (session_01GKuymoDm1XbC5G8TvaCNLr). Build master: BM19 (session_01GKuymncYhRTKs8t4byNfdj). W7 (session_01GKuymjghu82TGWPLR1wTKw; took over from W6) owns 24 core, 24u, section 28's shared helpers and the switch lines.
- **Pieces:** S6-2 M21 the Monday briefing (section 28b, `P5_M21`, 3 turns) now; S6-6 M24 leading a team (section 28d, `P5_M24`, 4 turns) in wave 2.
- **Branch:** `claude/p5s6-mech-a` from `claude/staging-p5s6` 64e296df. Build-table rows `0.94.0-s6.2a`, ... The build-number lines are never touched.
- **Overnight rules (lead 41):** no questions to the user; the spec's recommended answers; at most two browser checks at once (check_fast counts as two).

## Built (S6-2 turn 1)
- 28b: see DEV_NOTES "28b, M21 the Monday briefing". Not through the ladder (`WORK_MECH.m21.own`); two one-condition edits in 24 core (ladderTick's `ok`, What's next) skip an own row. W7 approved it (2026-10-27).
- Job slot 44 (`M21_SLOT`; 38 is P9_SLOT). schedU key 1070 (1070-1079 free for M21/M24 so far: 1070 used).
- Words: stand-ins baked by me (content/works/m21.lines, content/meetings/m21.brief.meet, m21.short.meet).
- Checks: mech_check part m21 (P5_STEP6 copy), controller_check part m21 (`P6_PARTS`, P5_STEP6 copy).

## Next
- S6-2 turn 2: day_check 22 and bigevents_check on a P5_STEP6 copy (the hold, no clash with the bridge invite at breakfast); the agenda screen tested live; the arrows_check step6 beat (the arrow-follower) if the frame exists by then; review fixes.
- S6-6 (wave 2): 28d, TEAM_JOBS.coil in 24h (the owner is W6 for the table's shape), slot 36.

## Gotchas
- `worksInit()` returns null before WORKS_START: in a test, skipTo first, then worksInit.
- `mailSend` unshifts: new Mail is at the front of SHIP.mail.
- In pad mode the arrow's label isn't the pad hint: read `goalNow().label` (with `GUIDE.key = ''`).

## How to test
- Setup: `pip install playwright numpy pillow`; three r128 and acorn into /tmp/cadet-work (testing-guide section 2); `CADET_CHROME=/opt/pw-browsers/chromium`.
- `python3 mech_check.py starship-cadet.html m21` and `python3 controller_check.py starship-cadet.html m21` (each makes its own P5_STEP6 copy).
- Off: `python3 cadet_test.py <64e296df build> starship-cadet.html` ALL IDENTICAL.
