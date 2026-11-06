# Handover: RV32 (reviewer, 0.99.7 playtest patch)

Session session_01GKuymkDX3gviqiGJcKLWuS, reports to lead 49 (session_01GKuymjjreuZtZeDMBX79xn). Build master BM24
(session_01GKuymnYTNkfxgLvtfFRg7w, claude/staging-0997): copy on every PASS with commit + game sha256.
Branch claude/review-rv32 (from claude/integration d7ad4c58 = 0.99.6, game f6ff5ec1...db8a8): notes plans/review-rv32.md
(every verdict), probes plans/rv32-probes/ (results/ beside them). Other reviewer RV33 (session_01GKuymoAK9gACR31MRd1CMX).

## Builders I review (from plans/patch-0997.md on claude/lead-49)
CH1 session_01GKuymjRkyieJLWiov9xvyp (claude/p997-chars), MV1 session_01GKuymmL8h3gYY1Td9gxV3n (claude/p997-move),
TP1 session_01GKuymneLr9U5MnEvACLMvS (claude/p997-tips), CR1 session_01GKuymizPyyNVZeZ2xUhGm6 (claude/p997-career),
JB3 session_01GKuymmiCEm3CMMrMTdWMEo (claude/p997-jobs).

## State (see review-rv32.md for detail)
- PASS sent: CH1 A 3d07e66; TP1 9c7a288 and a0e5dd5.
- CH1 B 8436ff6 (note 4): off identical, on check_fast/day_check OK, pictures fine; interactions_check (on) to finish.
- CR1: 2f2b93e no Day 8 test in a slipped week; fix 5d5acbf proven in the walk (Day 8 test passed 14:14). Still: off
  cadet_test + check_fast on for 5d5acbf, then PASS.
- JB3 43a96ae/e96ec5a: walk shows notes 21/22; to do: shelf fetch (note 3) probe, tea tap (JB3_TEA_ON), off identical e96ec5a, check_fast on.
- MV1 f2462cd: to do all: off identical (run twice: MV1 saw one differing run under load), briefing (with TP1's nd1 arrow),
  WASD at 390x844, rec toilets, clock tap.
- TP1 565a0da (nd1: Day 1 briefing/clock arrows, Day 2 meetings): to do: fresh walk WITHOUT FW_TRACK; off identical.
- Lead's open find: fresh save Day 1 08:45 had no arrow (0.99.6 too): TP1's 565a0da answers it.

## Kit and gotchas
- pip install playwright numpy pillow; three r128 + acorn 8.12.1 in /tmp/cadet-work (npm pack); CADET_CHROME=/opt/pw-browsers/chromium.
  Own CADET_WORK per run. Probes that exec cadet_test.py/arrows_check.py run from a worktree of the build (or repo root).
- fresh_walk.py: arrows_check's follower from a fresh save, intro on, 390x844; really sleeps (sleepGo) each night, closes
  the device, gets up from seats for an arrow. Env: FW_TRACK='1 08:25 Morning briefing' (a real tracker tap), FW_TRACE (JS
  logged on change), FW_UNTIL=HH:MM, FW_DUMP. Day N ends at (N-1)*1440 + 22:30. JSON only at the end: a restart loses it.
  A walk that never sleeps or leaves Mail open holds every tip (my first false alarm).
- interactions_check takes over an hour under load: give it a 2 h timeout, log in full (no grep pipe).
- The machine restarted once (09:05 UTC): /tmp survived, all runs died.
