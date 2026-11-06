# Handover: RV32 (reviewer, 0.99.7 playtest patch)

Session session_01GKuymkDX3gviqiGJcKLWuS, reports to lead 49 (session_01GKuymjjreuZtZeDMBX79xn). Build master BM24
(session_01GKuymnYTNkfxgLvtfFRg7w, claude/staging-0997): copy on every PASS with commit + game sha256.
Branch claude/review-rv32 (from claude/integration d7ad4c58 = 0.99.6, game f6ff5ec1...db8a8): notes plans/review-rv32.md
(every verdict), probes plans/rv32-probes/ (results/ beside them). Other reviewer RV33 (session_01GKuymoAK9gACR31MRd1CMX).

## Builders I review (from plans/patch-0997.md on claude/lead-49)
CH1 session_01GKuymjRkyieJLWiov9xvyp (claude/p997-chars), MV1 session_01GKuymmL8h3gYY1Td9gxV3n (claude/p997-move),
TP1 session_01GKuymneLr9U5MnEvACLMvS (claude/p997-tips), CR1 session_01GKuymizPyyNVZeZ2xUhGm6 (claude/p997-career),
JB3 session_01GKuymmiCEm3CMMrMTdWMEo (claude/p997-jobs).

## State (2026-11-06 ~09:55 UTC; see review-rv32.md)
- PASS sent: CH1 A 3d07e66; TP1 9c7a288, a0e5dd5; JB3 e96ec5a (to JB3, lead, BM24).
- CH1 B 8436ff6 (note 4): off identical, on check_fast/day_check OK, pictures fine; interactions_check (on) rerunning
  (/tmp/rv32/ch1b_ix_full.txt; it timed out once under load, then the machine restarted).
- CR1 3e1b0dc (game c61bda34...180791; switches false; catch-up + m6 needs only m1 from Day 8): off identical; walk to Day 9
  (/tmp/rv32/fw_cr1c.txt) and check_fast on (/tmp/rv32/cr1c.txt) running. 5d5acbf's walk passed the test Day 8 in a slipped week.
- MV1 2e268ba (game 4558720e...b55af): f2462cd failed machine_check (food runs) with MV_RECWC_ON; 2e268ba makes the rec
  toilets yours only (schedData skips p.you: Sim engineer to look). /tmp/rv32/mv1c.sh: off cadet_test, MV1's probes, check_fast on.
  Still mine: a briefing check in a fresh walk (MV_BRIEF_ON: the Chief stays to the end), WASD at 390x844 by real keys.
- TP1 c920acb (game c9a2a32e...47bda4; TP997.nd1 arrows + needs yield in week 1): fresh walk with NO tracker tap
  (/tmp/rv32/fw_tp1d.txt): Day 1 briefing met via its arrow, Day 2 office meeting and Zeke's 10:45 met. Still: off
  identical, check_fast on, then PASS.
- Next idea (lead's call): MV1's briefing fix and TP1's briefing arrow together in BM24's staging build.

## Kit and gotchas
- pip install playwright numpy pillow; three r128 + acorn 8.12.1 in /tmp/cadet-work (npm pack); CADET_CHROME=/opt/pw-browsers/chromium.
  Own CADET_WORK per run. Probes that exec cadet_test.py/arrows_check.py run from a worktree of the build (or repo root).
- fresh_walk.py: arrows_check's follower from a fresh save, intro on, 390x844; really sleeps (sleepGo) each night, closes
  the device, gets up from seats for an arrow. Env: FW_TRACK='1 08:25 Morning briefing' (a real tracker tap), FW_TRACE (JS
  logged on change), FW_UNTIL=HH:MM, FW_DUMP. Day N ends at (N-1)*1440 + 22:30. JSON only at the end: a restart loses it.
  A walk that never sleeps or leaves Mail open holds every tip (my first false alarm).
- interactions_check takes over an hour under load: give it a 2 h timeout, log in full (no grep pipe).
- The machine restarted once (09:05 UTC): /tmp survived, all runs died.
