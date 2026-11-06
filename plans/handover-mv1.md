# Handover: MV1 (movement, crew walking, needs) for the 0.99.7 playtest patch

Role: builder MV1 for lead 49 (session_01GKuymjjreuZtZeDMBX79xn); reviewer RV32 (session_01GKuymkDX3gviqiGJcKLWuS).
Branch: `claude/p997-move`, from claude/integration d7ad4c58 (0.99.6, game f6ff5ec1...db8a8).
Notes: plans/patch-0997.md on claude/lead-49, notes 2, 5, 19, 24, 45 (the user's words are there).

## What was built (all behind switches, all off: cadet_test ALL IDENTICAL against d7ad4c58)

The six switches are on one line in section 13, just above `function saveGame()` (var, because 4e and 15 read them at load).
Switching one on is changing its `false` to `true` there.

| Switch | Note | Where | What it does |
|---|---|---|---|
| `MV_BRIEF_ON` | 2 Chief walks away during the morning briefing | 21 (`INTRO_WEEK` 'd1-briefing' gets `release`, `keep: 70`), 21b slot (`introKeep`), `introWeekBeat(b, id)`, `introReleased` | Day 1's briefing: the Chief's block runs until the meeting's panel closes (cap 10:15), 09:05 as before if you missed it; she stands at 5-works-bay-lead-1 [16,0], not on the time clock (backlog MV1-2) |
| `MV_WASD_ON` | 5 WASD walks | 11 (`updateSteer` calls `keyWalkStep`; code in the HUD seat slot) | W, A, S, D and the arrow keys steer you like the controller's stick; not with a panel open, paused, riding, typing, or with Ctrl/Alt/Cmd |
| `MV_FIT_ON` | 19 fitness drops faster | 15 `NEED_DRAIN.fitness` | 0.9/0.3 an hour to 1.8/0.4 (about 17 to about 32 a day) |
| `MV_RIG_ON` | 24 crew flash far from the lift | 10 `crewDetail` | a new full rig (story crew within 4.5 tiles) is posed at once; it was drawn one frame at the deck's origin |
| `MV_SOFA_ON` | backlog EV1-1 (lead's add): tapping a seated host to join stood them up | 10 `crewWayOn`, `CrewAgent.update`'s make-way test | a crew member settled in their own seat only moves aside for the seat's own tile, and your seat's walk tile isn't kept clear while you sit; stations unchanged |
| `MV_RECWC_ON` | 45 rec deck toilets unusable | 4e `place('u', 'toiletStall', ...)` gets a Toilet card; 4e slot `recWcPlaces()`, called from 13 after the switches | 7-toilet-1..4 and 7-basin-1..2 in room 'u'; the red stall lights work; the rec crew can take toilet breaks there |

Checks changed: player_check expects about 32 a day with `MV_FIT_ON`, 17 without.

## Causes (short)
- 2: her block ended 09:05; the meeting starts any time up to 09:05 and its script runs about 80 real seconds (about 50 ship minutes at SHIP_RATE 0.6). Reproduced: off, she goes to the toilet at 09:06 mid-talk.
- 24: `crewDetail` makes a `FullPerson` (scene.add at 0,0) and only the next frame's update places its root. day_check's `bornFar` reads `Human.set`'s pos, not the drawn root, so it missed this.
- 45: the stalls had no places and no card.

## Probes (tools/mv1/; each takes the build's path; they chdir to the repo, run with CADET_CHROME set)
- `lift_probe.py BUILD '[[3,1,1080]]' 1800`: every on-screen crew body's drawn root each frame; off shows Vance, Saruth, Marrow at r [0,0]; on shows none.
  The remaining small flags (0.3-0.5 off) are the crowd's every-few-frames posing and queue shuffles, not lift-related.
- `brief_probe.py BUILD attend|late|miss`: Day 1 in the real game (intro on), the briefing read at about 3 s a line, where Calder is.
- `wasd_probe.py BUILD`: real key presses at 390x844: direction against the screen, release, device open, text field, Ctrl, pause.
- `sofa_probe.py BUILD`: Vance held on 3-lounge-25, you sit on 3-lounge-26 (same walk tile): off he's sent aside as you set off; on he stays seated.
- `m21_probe.py BUILD`: 28b's Day 22 briefing at about 3 s a line (fine: ends 08:56 of 09:15).
- `clock_probe.py BUILD [during]`: Day 1, taps on the time clock during and after the briefing: off they open her chat; on, the clock.
- `wc_use.py BUILD`: the rec deck's places, stall lights, a toilet and a basin used by tap.

## Test results (switches on, in a copy)
player_check OK, interactions_check OK, day_check Day 6 OK (deck 7 peak 176 calls), intro_check: see the message to the lead.
Switches off: cadet_test ALL IDENTICAL, check_fast OK.

## Loose ends, questions for the user
- Note 5: arrow keys walk too (default yes). The walk tip still says "Tap where you want to go, or press and hold"; a keyboard line could be added by TP1 if wanted.
- Note 19: about 32 a day is the lead's default; the user may want a different number.
- Backlog MV1-2: fixed under MV_BRIEF_ON (her spot), at the lead's ask.
- Backlog MV1-1: the Monday briefing (28b): Day 22's full one probed, fine; the short later one (20 minutes) not probed.
