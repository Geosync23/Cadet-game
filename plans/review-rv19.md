# RV19 review: 0.93.2 (bunk inspection, save slots)

Reviewer RV19 (session_01V6FDCQp5Ejidi8Chpo2nJG), hired by lead 38 (session_01G2y9crUv6vDiiEB2q6Yo9W). Every verdict goes to
lead 38, BM18 (session_01A3S2VBMYmTt2wCZa8ej7XR) and the builder with the exact sha. Notes only, branch `claude/review-rv19`.
Base: claude/integration b957b92d (0.93.1, game sha256 6cd54ab9...8eee).

1. FX20 (session_01FdWDetSihcXZYe2Tp8Kgjy), `claude/inspection`, switch `INSPECT_ON` (ON in 0.93.2).
2. FX27 (session_019Qp5uSM5piXqZXYFENDvkK), `claude/save-slots`, switch `SAVE_SLOTS_ON` (ON in 0.93.2).

The user's rule for the inspection: "Bunk inspection doesn't do anything. A supervisor should come by." It must visibly do
something: someone actually comes by.

## FX20, the bunk inspection: 03449ace (0.93.2-i.5, game sha256 dcb4060a...5157; switched-on copy ba57eaa1...18be)

Diff read: section 4d (INSPECT_ON, INSPECT_ROOMS / T0 / STEP, inspectPass, inspectWalker, the stand spots made only with
the switch on), section 14 (STOPS gets 'inspect'; schedFrame's two wake lines; morning(): the stand-first, the walker's
route, the junior's stand), section 22 (SW2's words, baked), section 24c (inspectOfficer, inspectWalkerAt, inspectWalkTick,
the WORK_TICKS line), day_check's part. Everything is behind INSPECT_ON. Nothing calls R() at load; inspectWalker reads
the calendar only (schedPeople, isWorkDay, schedU), so the planner may ask it.

### Checks
| Check | Build | Result |
|---|---|---|
| cadet_test vs b957b92d, alone | 03449ace off | ALL IDENTICAL |
| check_fast (words, names, deck, machine, leave, device) | 03449ace on | QUICK CHECK OK in 542 s |
| day_check 4 | 03449ace on | FAILED: only its own inspection line (M1); schedules 0/0/0/0/0, nobody stuck, draw calls under 450 |
| day_check 11 | 03449ace on | DAY CHECK OK (walk planned a@06:19-06:35, then 5 min a room; 30 of 46 juniors stand) |

### Played at phone size (390 x 844), switch on, the player at their bunk in Bunk 1 from 06:00
A probe steps each ship minute 06:00-07:20 and records the walker's room, their target spot and distance to it, the
juniors at their stand spots, every worksSay and toast, the inspection note and the Mail.

**Day 4, Calder.** Down at 06:04, in Bunk 1 from 06:14 (early, standing there). 06:30 "Morning, Bunk 1. Stand by your
berths, please." then at 06:31 the result in person ("Two out of three...") and Tomas's training toast. 24-26 juniors at
their stand spots, real and visible. This part works and meets the user's rule. Then: Bunk 2 at 06:38, Bunk 3 at 06:43;
from 06:45 she is in the corridors the whole time: target d at 06:45-06:50, e at 06:50-06:55, f, g, h, and she never
gets into Bunks 4-8 (room codes only `+`, `=`) before the walk ends at 07:10. In the phone shot
at 06:31 her bubble is clear over the bunk room, the juniors in a row by their bunks.

**Day 11, Mira Dahl** (cabin 4-17, on Deck 4 already). Washes at 4-basin-p1 until about 06:19, then heads for Bunk 1: at
06:30 she is 9.6 tiles away in the corridor, at 06:35 4.5 tiles away, and her target turns to Bunk 2. **She never enters
Bunk 1.** The player, standing at their bunk all along, gets nothing in person and at 06:59 the Mail ("Two of the three
weren't right..."), note `here: false`, so the attendance isn't counted (worksUse only on a nod). Bunk 2 at 06:37, Bunk 3
at 06:43, then the same corridor chase as Day 4: Bunks 4-8 never reached.

### Findings
**Must**
- M1. day_check 4 fails on FX20's own line at 03449ace: i.5 moved the walk's start ("leaves for Deck 4 at about 06:05"), so
  the room-a segment begins at 06:05 (365) and the check's `walk[0][1] < 370` fails. Update the check to what it means
  (the walker at room a by 06:30; the walk done by 07:15), and check_fast plus day_check 4 and 11 green.
- M2. The walker never reaches Bunks 4-8 (5 of 8 rooms), Days 4 and 11. The order a..h zigzags across the deck
  (a 8,3; b 13,3; c 17,3; d 8,16; e 10,6; f 10,13; g 15,6; h 15,13: c to d is about 15 tiles, then back up to e, down to
  f...) and each room gets a fixed 5 minutes, so from c on the walker is always behind: the next segment starts before
  they arrive and they turn round in the corridor. The juniors in d-h stand and are released without anyone coming. The
  plan looks right on paper (day_check reads the plan only), the drawn game doesn't. Fix: a route that follows the deck
  (e.g. a b c g e f h d, or whatever path is shortest), and each room's time from the real walking time (arrive, then
  INSPECT_STEP there), with the juniors' inspectPass taken from the same times. Prove it live: the walker inside each
  room for at least a couple of minutes, Days 4 and 11 (and one more rota week).
- M3. A player who is at their berth can be marked absent (Day 11 above). The in-person result needs the walker inside
  room a while still targeting 4-inspect-a, a 06:30-06:35 window; a walker who is late (Mira's wash, a lift wait, a
  crowded corridor) gives a Mail and no attendance to a player who did everything right. Two parts: (a) the walker must be
  in Bunk 1 by 06:30 (no wash or other stop planned between 06:05 and the walk; down earlier from another deck or
  cabin); (b) a safety net in 24c: if you were in your bunk room from 06:30 and the walker hasn't come by 06:59, still
  count it as attended (here: true) and say it in person when they arrive, or by the Mail worded for someone who was
  there, never the "you weren't there" path.

**Should**
- S1. SW2's room lines (`inspect.walk.room.b`..`h`) and `inspect.walk.done` can't be heard on the normal path: the WORK_TICKS
  line returns as soon as `inspectDue(d)` is false, and it is false straight after your own result (room a, first). So a
  player who attends and then follows the walker hears nothing more, and the done toast (after Bunk 8, 07:05+) never
  shows (by then the 06:59 Mail has also run). Run inspectWalkTick while `INSPECT_SAID.d === d` / the walk is on
  (06:30-07:20), not only while the inspection is due; keep inspectRun's own guard as it is. Both days above: only the
  arrival line and the result were said.
- S2. The walker's "look pose": `anim: 'look'` isn't in ACTS (section 26's animations: row, cycle, run, ... talk), so the
  walker just stands; the probe reads no anim on Calder or Mira. Use an animation that exists (e.g. 'read' with a clipboard
  or datapad look, or add a small 'look' turn of the head and torso to ACTS in its owner's slot), and say which.
- S3. day_check's inspection part reads only the plan; add a short live part (or a new small check) that steps 06:00-07:20
  on Deck 4 and checks the walker is inside each room in order, so M2 and M3 can't come back unseen.
- S4. The handover note says INSPECT_STEP 3 and the walk 06:29-06:54; the code is 5 and 06:30-07:10. Keep the note in step.

**Verdict on 03449ace: FIXES NEEDED (M1-M3).** Off is exactly 0.93.1; the Bunk 1 visit on Day 4 works and looks right
at phone size.
