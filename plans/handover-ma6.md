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

## Turn 2 (checks only)
- day_check 22 OK (plain and forced copies), bigevents_check OK, controller_check m21 adds the wall screen. RV23 PASS on 27166be.

## State (2026-10-27 ~12:40 UTC)
- All my work is in claude/staging-p5s6 ce113792: S6-2 (27166be, RV23 PASS) and S6-6 turns 1-2 (8f943e82, a92d0562, RV23 PASS), plus test-only commits.
- Left: the arrows_check step6 beats for the briefing and night 3 once that frame exists (S6-3's, W7); the head writer's words replace my stand-ins (m21.lines, m21.*.meet, m24.lines; keys as they are). Known, low risk: Vance is in the briefing's cast; if the bridge invite (Vance at breakfast, 05:00-10:00) ever fell on a briefing Monday he'd be pulled to Deck 1 at 08:30.
- Backlog MA6-1 (team turns can't be tapped) is PZ6's fix (claude/team-turn-fix); the coil swap doesn't depend on it.

## S6-6 turn 1 (M24)
- See DEV_NOTES "28d, M24 leading a team". Slot 36, schedU 1071. DA6 (session_01GKuymjJ4sU5hfdU8bH49UW) owns S6-4: coils '6-coil-1..3', spots '6-coil-team-1..3' (spot 1 the lead's: yours). N6 (session_01GKuymnDA25R2a5yZGYpaBS, claude/p5s6-nights) asked about night hooks (no reply yet). W7 asked about the 24h table entries (no reply yet). Backlog MA6-1: a team turn can't be tapped in today's game.

## S6-6 turn 2
- N6 answered: playerNightOn(d), yourShift(d).night, p5nIn(t), SHIP.works.ns[d]; night 3's incident a burst on Deck 5 at 02:30 Day 25 (the Watch's hour avoids 02:30-03:30); 28a calls 28b's m21Door() if defined. W7 OK'd the 24h entries (and asks that Step 6's Dev table rows are his alone: told him m21/m24's facts). DA6's coils/spots work (checked on a scratch merge of claude/p5s6-deck dd32a9a7). RV23 PASS on 8f943e82.

## Gotchas
- simNote keeps only its own kind: a payload's `kind` (24h's 'turn', 'step', 'done') is overwritten with 'team'; read step numbers.
- Line keys allow no underscores (content_gen's kind pattern); placeholders only from lines_check's PLACEHOLDERS.
- `worksInit()` returns null before WORKS_START: in a test, skipTo first, then worksInit.
- `mailSend` unshifts: new Mail is at the front of SHIP.mail.
- In pad mode the arrow's label isn't the pad hint: read `goalNow().label` (with `GUIDE.key = ''`).

## How to test
- Setup: `pip install playwright numpy pillow`; three r128 and acorn into /tmp/cadet-work (testing-guide section 2); `CADET_CHROME=/opt/pw-browsers/chromium`.
- `python3 mech_check.py starship-cadet.html m21` and `python3 controller_check.py starship-cadet.html m21` (each makes its own P5_STEP6 copy).
- Off: `python3 cadet_test.py <64e296df build> starship-cadet.html` ALL IDENTICAL.
