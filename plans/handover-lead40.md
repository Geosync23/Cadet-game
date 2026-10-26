# Handover: lead 40

## START HERE (next lead)
Read CLAUDE.md, this note, then the bottom of TEAM.md on claude/lead-40 (from "LEAD 40 started", ~22:00 UTC Oct 26). plans/handover-lead39.md has the background (user rules, specs, ending answers) and still holds.
Lead 40 = session_01NXybH7NNqM8M4ngiyidq6m, branch claude/lead-40 (from claude/lead-39). Hourly check-in trig_01Ho4S7S9dCaYyVC7qSaQi9t (57 * * * *): disable it when you take over and make your own.

## Why this stopped
~23:45 UTC (7:45 PM Eastern) Oct 26 the user called a STOPPING POINT: they may move to another account and have not decided. Every seat was told to finish only 0.93.3, start nothing new, push work-in-progress and update its handover. **Do not restart work until the user says whether we continue on this account or transfer.**

## User rules (unchanged, see handover-lead39.md)
Keep reducing the workforce (archive as soon as a piece passes + handover pushed; replace, don't add). Tons of arrows, staged scenes with dialogue, every piece works with a controller. Times to the user in US Eastern. No emojis. Never publish over 6daNCLCJAcsLCZn27CEthq.

## Releases
- LIVE before this stop: 0.93.2 (Playtest 3HqM v6, Dev 9ZWA v6).
- **0.93.3** (staging-0.93.3 19400976, game ec93b94d...d085: doors 3 ways + visit on + SW2 words + check fixes): full round all 6 shares OK, no new FAIL. perf_check flagged 3 single-scene js-time blips (backlog 32 pattern); CR4 re-measuring. On GO, PUB1 publishes both links as v7 (keep {downloads}). Check TEAM.md for whether this happened before the stop.
- **0.93.4 (NOT started)**: published 0.93.3 + B2 claude/workstep-tap-fix c79a66dc (LIVE M15 Rewiring tap bug; RV20 PASS) + b7e84f81 on top (stale team-job arrow, live; RV20 pending) + FX30 test-only fa6b7de0 (week guide; CR1 OK on 0.93.3). Full round, then publish.
- ff integration only with the user's OK.

## Work in progress (all switched off in the game)
- **Step 5** (P5_STEP5): RV20 PASS: SW3 words, B4 puzzles 6b07b624 (via RV21), B3 M20 7c5d9f79 (via RV21, 4 shoulds). Waiting on RV20: B5 promotion claude/p5s5-promo e7ff9253 (includes B1 51b1a9c6, VB2 kit 69eb706d: collar bar + Calder's visitor chair, teacher-at-meeting fix for every lesson); B2 M19 claude/p5s5-mech-a deefa61a; B3 S5-4 claude/p5s5-mech-b 7e6bca4b. B3 M20 shoulds on claude/p5s5-m20 (newer than f57afcbc) -> RV22. On promotion PASS: early Dev link ?p5s5 for the user (user already said yes).
- **Vessel** (EV_VESSEL_ON): V-1..V-4 RV21 PASS (claude/vessel 6d4b5192). VB1 doing shoulds (ramp crowd, goodbye window, round-one fallback, Saturday Calder comes to you, doubled toast, setTimeout) + merge VB2 vessel-sky 3fb8eac7 + arrows_check part + controller presets -> RV22.
- **Ending** (EV_ENDING_ON): RV21 PASS as one, claude/ending-crossing d1a61402. VB2 owns it now: arrows_check endstay/endgo + controller presets + day_check 31/50 ON copy (claude/ending-checks) -> RV22.
- **Step 6**: not started; reuse Step 5 seats (VB2 earmarked S6-4 deck architect; B3 free).

## Seats at the stop
Active: BM18 01A3S2VBMYmTt2wCZa8ej7XR; PUB1 01GnpjFR6oumvuvTrmcXSqeg; RV20 01PyJwfvfQVu4oXTYDMGkacw (~48%+); RV22 011wAn842cKDVWvoH8Cr9geD (new, replaces RV21); CR1 01CsWNjCsy8u5mrHJgTVgCst, CR2 01DsTDi6xJcpdDVhSkELEm24, CR3 01Pw3EQ24pSz4gjsFcLBMjUF, CR4 01RgnU5d6Um75LNznFSotXYH, CR5 01UH1U1UpsoL7viYaRRBu2bZ, CR6 013wLtAmKooMrgGrXF4Ljiof; B2 015mjNkxuGoEZGKA2ksBPz9u (~60%, archive on RV20 PASS); B3 014FBmsiTsA9QymoN2qt4NyL (~45%); B5 01CgbXRamJJp66pFTP43KYoB (owns 24 core/24u); VB1 01UsjGN26E88zwrNPWwef4iT (~45%); VB2 01KRBGtugjBpv5iGcV5WDvCP (~40%). Lead 39 019V68fz33UFv4cK5Z4iCDvi idle (archive).
Archived by lead 40: EN1, B1, FX30, EN2, B4, RV21 (24 closed since lead 39 started).
If moving accounts: these sessions stay on this account; a new account starts fresh sessions from the branches and handover notes named above.

## Backlog added this shift
P9 true move needs a second section 14 hook after schedBuild (B4-1); interactions_check.py:1262 SyntaxWarning '\|' (test only); careerOff read live (only matters if section 14 plans Monday's shift before Sunday's settle); perf blips (backlog 32) if they repeat; social/device owners' one-line hook reviews for the ending.

## Waiting on the user
Continue here or transfer to another account. Tap-test Download my save / Load a save file ("later").
