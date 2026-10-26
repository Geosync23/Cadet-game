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

### After the verdict
- FX20's final sha was f3cd2a9e (game unchanged from 03449ace); M1 done in eb87ab31 (day_check's start bound 355, check only).
  Note for the fix: the check's `order != list('abcdefgh')` must follow M2's new route. FX20 retired at ~66%; lead 38 hired
  FX20b for M2, M3, S1, S2 on claude/inspection (handover 9137785e carries these notes). The probe is
  plans/rv19-probe-inspect.py on this branch.

### Re-review: FX20b (session_01ForKrDZQQCL59hA3yZDfD3), 9b7eae69 (game = 0bc18dc, sha256 29fd2411...4b1c; on copy c2e937ea...f1f8)
Diff read (vs 03449ace): 4d INSPECT_ROUTE (a e b g c h f d, each leg's tiles), INSPECT_TIMES / inspectPass from it,
inspectWalker skips anyone not aboard; 14 schedFrame (the walker in bed by 22:40 the night before), morning() (the walker's
own block: a 5-min wash only if done before set-off, set-off from walkLead, each room's door till inspectPass; the juniors
in their bunk till 10 min before the walker's due, then stand); withHold gives the walker the officers' datapad at each
4-inspect place (the 'look' anim gone); 24c inspectWalkDo (words for the whole walk, the result in person when the walker
reaches your room with you in it, there-from-06:30 safety net at 07:20 as their word, never the Mail). Off: the WORK_TICKS
line returns into inspectWalkDo only with INSPECT_ON; the old two lines are unchanged. Nothing calls R() at load.

| Check | Build | Result |
|---|---|---|
| cadet_test vs b957b92d, alone | 9b7eae69 off | ALL IDENTICAL |
| check_fast | 9b7eae69 on | QUICK CHECK OK in 559 s |
| day_check 4 / 11 / 18 | 9b7eae69 on | DAY CHECK OK, all three; schedules 0/0/0/0/0; worst stuck 0.2 ship min; draw calls peak 345 |
| day_check's new live part | same | a@06:20-06:23 (in 10-13 min), then e 06:36, b 06:41, g 06:45, c 06:49, h 07:01, f 07:07, d 07:12, 2-3 min inside each, all three days |

Played (my probe, 390 x 844, a ship minute at a time):
- Day 11 at the bunk: Tove Cruz in Bunk 1 from 06:10; 06:30 "Right, Bunk 1. Let's have a look at you."; 06:31 the result
  in person (note here: true); no Mail. Then every room in route order, inside each 1-3 min; done toast 07:14. (M3 fixed.)
- Day 4 following the walker room to room: Calder's arrival and result in Bunk 1, then a line in every room (Bunk 5, 2, 7,
  3, 8, 6, 4) and the done toast at 07:14. (M2, S1 fixed.) Bubbles at phone size over the room, readable.
- M1 and S3: day_check checks the route, the plan's times and the live walk; S2: datapad; S4: handover note updated.

Notes (not blocking, no change asked):
- N1. With the juniors up only 10 minutes before the walker's due, 4-10 are standing in the room being visited (8 in Bunk 1).
  Enough to read as an inspection; a tuning item if the user wants a fuller line-up.
- N2. In my Day 4 follow shots the bubbles in Bunks 2 and 3 are dimmed: Tomas's Day 4 card was still open (my probe's
  setup jumps straight to the morning without closing it). Not judged.

**Verdict on 9b7eae69: PASS.**

## FX27, save slots: ba6b7b9a (game sha256 d7b6a9f4...2e09; first push 756b86d3)

Diff read: section 13 (SAVE_SLOTS_ON, SAVE_BASE, slotKey, slotRead, SAVE_SLOT and SLOT_NEW read once at load, SLOT_HOLD in
saveGame, saveOk split out of loadGame with the same checks plus `typeof s === 'object'` and `!p`), section 19 (the Saves
app: slotInfo, slotPlay / slotNew / slotDelete / slotGo, slotDownload / slotCopy, slotPick / slotFile / slotLoadText /
slotPut, the view; `s.at` in SAVE_EXTRA only with slots on and saving), section 21 (INTRO_BOOT with SLOT_NEW; Monday skips
the arrival), section 25 (dmRealKey: Copy my real game copies the Playtest slot being played). Slot 1 keeps the old key
for both links, so nothing is copied or moved. The Load button's file picker and the copy run straight from the button's
click (deviceDo from onclick), so the browser's user-gesture rule holds. Download on claude.ai follows the platform's
downloads contract (runtime 0.2.91 downloads.d.ts: `claude.use('downloads')`, `save({ filename, data })`, `.json` on the
allowlist, `declined` and `rate_limited` handled, anything else falls back to Copy save as text).

| Check | Build | Result |
|---|---|---|
| cadet_test vs b957b92d, alone | ba6b7b9a, SAVE_SLOTS_ON false | ALL IDENTICAL |
| cadet_test vs b957b92d, alone | ba6b7b9a as pushed (on) | ALL IDENTICAL (renderer noise only; tests use ?nosave) |
| check_fast | ba6b7b9a | QUICK CHECK OK in 521 s |
| saves_check (all parts) | ba6b7b9a | SAVES CHECK OK |
| devmode_check | ba6b7b9a | DEVMODE CHECK OK |
| RV19's own (plans/rv19-slots-check.py), 390 x 844, one http origin | 0.93.1 then ba6b7b9a | RV19 SLOTS OK |

RV19's own check, with the real 0.93.1 build (not the switched-off copy) writing the saves:
- 0.93.1 writes a Playtest save (Day 6 13:10) and a Dev save (Day 15 08:20). The new build on the Playtest link: Slot 1,
  key starship-cadet-save, the game loads at Day 6 13:10, the save byte for byte at load, the Dev save untouched, no slot
  keys made; the Saves app lists Slot 1 (playing), 2, 3. On the Dev link: Dev Slot 1 (starship-cadet-save-dev), Day 15
  08:20; playing there leaves the Playtest save alone.
- A broken -slot key ('abc', '7', '0', '2.5', '-1') plays Slot 1 every time.
- Bad files refused with "That isn't a Starship Cadet save file, so nothing changed." and storage byte-identical, no card
  opened: not JSON, empty, a JSON array, v 3, no player, deck 99, another JSON file.
- A file that passes saveOk but holds almost nothing ({ v, time, player }) starts the game without page errors, with the
  device (so the Saves app) reachable: a thin file can't lock the player out of their other slots.
- After all of it, Slot 1 still the old Day 6 game.

Phone look (saves_check's shot, 390 x 844): the slots, Play and Delete, readable; Download and Load a save file below,
reached by scrolling the app. "Last played 1 Jan 1970" in that shot is the checks' frozen clock (cadet_test sets
Date.now to the virtual time), not the game.

Notes (not blocking):
- N1. Inside a real claude.ai artifact page I can't press the platform's download confirmation from here (it needs a
  viewer). The code matches the contract and saves_check mocks it both ways. For the release: BM18 must publish 0.93.2
  with `capabilities: { downloads: true }` (FX27 told the lead), and someone opens the published page on a phone once and
  taps Download my save, then Load a save file with that file.
- N2. slotWhen shows any number as a date: a save from a browser with a wrong clock would say an odd "Last played". Only
  cosmetic.
- N3. The arrival flag (starship-cadet-arrived) is per link, shared by the three slots. It only matters for a slot with no
  save, and New game in a slot sets SLOT_NEW, so nothing goes wrong; worth knowing for whoever touches section 21 next.

**Verdict on ba6b7b9a: PASS.**

## FX28, promotion beats (claude/promo-beats, PROMO_BEATS_ON)
Added by lead 38 at 05:07: the Tier 2 test and promotion made "very very hard to miss" (the user). Lands in steps over
about 9-10 h; each step reviewed as it arrives, every one on a phone-size screen. Not pushed yet.
