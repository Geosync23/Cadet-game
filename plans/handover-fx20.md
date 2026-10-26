# Handover: FX20 (builder), 2026-10-26

Written at about 58% memory, updated at about 65% (2026-10-26 ~05:00 UTC). Lead now: lead 38 (session_01G2y9crUv6vDiiEB2q6Yo9W, took over from lead 37). Reviewer: RV19 (session_01V6FDCQp5Ejidi8Chpo2nJG). Build master: BM18 (session_01A3S2VBMYmTt2wCZa8ej7XR). INSPECT_ON is to be ON in 0.93.2 (lead 38).

## Current job: the bunk inspection walked for real (0.93.2)

The user: "Bunk inspection doesn't do anything. A supervisor should come by." Branch `claude/inspection`, from `claude/integration` b957b92d (0.93.1). HUD `0.93.2-i.N` (i.5 now; branch head eb87ab31, game as 03449ace). Reviewer RV19. Words: SW2 (session_017dLaLFBnRUQin3PQEQq6so), CS1 checks.

### What's built (all behind `var INSPECT_ON = false`, defined beside the inspection places in section 4's Deck 4 data, so the planner sees it)
- `inspectWalker(d)`: from the calendar only (the planner may not read live state): Calder in week 1 (Day 4 is the first inspection Thursday; the m3i row's fixed day is 4) if she's on shift, else an officer/senior/chief on a day shift that day, by the week's rota (schedU(864, week, 864)).
- Section 4 data: with the switch on, a stand spot per junior bunk, `<bed>-stand` (event places, the tile in front of the bunk, two per tile offset ±.22).
- Section 14 (planner):
  - schedFrame: on inspection Thursdays the walker wakes by 05:30, the day-shift juniors 05:30-06:00 (spread).
  - morning(): the walker goes to Deck 4 and straight to `4-inspect-a`, then a..h, `INSPECT_STEP` (5) minutes each from 06:30 (sets off for Deck 4 about 06:05: walking is slow at ship speed) (tag `inspect`, anim `look`; `inspect` added to `STOPS` so it never stretches). A junior stands at their stand spot until `inspectPass(room)` + 1. If that's within 30 minutes they stand first and wash after (`stood`). Otherwise there's the old 10-minute tidy.
- Section 24c: `inspectOfficer` returns the walker when on. `inspectWalkerAt(d)` gives the room the walker is in (heading to its door spot). `inspectWalkTick` says the words:
  - the arrival line in your room, then your result in person (inspectRun(d, true), 2.6 s later);
  - a line per other room while you're in it;
  - a heads-up toast if they reach your room and you're elsewhere;
  - a "done" toast after Bunk 8.
  The 07:00 Mail is as before.
- Words: SW2's content/works/inspect-walk.lines (CS1 PASS), baked in i.3 (worksText keys, variant by week): `inspect.walk.arrive`, `inspect.walk.room.b`..`h`, `inspect.walk.away`, `inspect.walk.done`. 
- `day_check.py`: on an inspection morning with the switch on (run on a switched-on copy), the walk in order a..h between 06:25 and 07:00, at least 25 juniors standing, and no stand spot used twice.

### Measured
- Day 4 walker Calder, Day 11 Dahl Mira; route 06:29-06:54. 30 of 55 juniors stand: the night shift's Bunk 8 sleeps (by design), and some juniors are already at early work stints.
- Live (scratch probe): Calder in Bunk 1 by 06:30; "Morning. Let's see." then the result in person (simNote here: true); Tomas's training as before.

### Checks (on i.5 03449ace / eb87ab31)
- Done: check_fast OK; cadet_test switched off vs b957b92d ALL IDENTICAL; switched on: day_check 4 OK (walk a@365-395 then 5 min each to 07:10, 31 of 46 juniors standing), player_check OK (0 fails), interactions_check OK (on i.4); live probe Day 4: Calder in Bunk 1 at 06:30, "Morning, Bunk 1. Stand by your berths, please.", your result in person. day_check 11 was still running at this update.
- Tuning item: at ship speed the walker spends much of each 5 minutes walking between the far rooms (seen in rooms a and c at six-minute samples), so the other rooms' lines come only when you're in a room as they pass.
### (older list)
- check_fast; cadet_test switched off vs b957b92d (must be ALL IDENTICAL).
- On a switched-on copy (`sed 's/^var INSPECT_ON = false;/var INSPECT_ON = true;/'`): day_check 4 and 11, player_check (3 known reserved-job FAILs exist on 0.92.6 too: compare), interactions_check.
- Then push, and send the sha to lead 37 and RV18 (and SW2's words when they land).

### Loose ends / ideas
- The juniors stand facing out of their bunk; their pose is `stand` (no salute anim exists).
- `inspect.walk.done` fires 4 s after the walker enters Bunk 8 while you're on Deck 4.
- A design-doc line (Thursday inspection: now walked by the duty officer) goes in with the switch-on decision.

## Earlier work (done, reviewed)
- 0.92.6 item 10, odd jobs (`ODD_ON`, claude/p926-fx20, RV15 PASS).
- 0.93.0 activity sounds (claude/sound-act 7e63f194, RV17 PASS). plans/sound/audio-todo.md lists what's left for the listening pass (dryer, airlock, shuttle bay).

## Gotchas
- In section 27 (sound) the core's `S.actTick = null` and `S.whenReady` come after the activity slot. Install from `S.onFrame` once.
- Use `pgrep -f "[n]ame"` in wait loops, or the loop matches itself.
- Each parallel check needs its own CADET_WORK with `three` and `acorn` links.

## RV19's verdict on 03449ace: FIXES NEEDED (2026-10-26 ~05:15 UTC; full notes plans/review-rv19.md on claude/review-rv19)
For the fresh seat. FX20 stopped here at ~66% memory, and nothing below is done unless marked.
- **M1** (done in eb87ab31): day_check's start bound was 370; it's 355 now. RV19 would rather the check test what it means: at room a by 06:30, done by 07:15.
- **M2** (open, the big one): live, the walker never gets into Bunks 4-8, because the a..h order zigzags (c at 17,3, then d at 8,16, then e at 10,6...) and 5 fixed minutes a room can't cover the walk. Suggested fix:
  - Order the rooms along the deck. From the places' `at`, a,b,c are on row 3 and e,g on row 6 (the north side); f,h on row 13 and d on row 16 (the south side). So try a,b,c,g,e,f,h,d, or measure the path lengths with findPath between the inspect places.
  - Give each room its time from the real walking time: the path length in tiles divided by crew speed in tiles per ship minute, measured live, plus the step at the door. Compute these once from the places, deterministically, and use the same times in `inspectPass` so the juniors are released only after the walker has really been.
  - Prove it live (RV19 has a probe that steps each ship minute and logs the walker's room).
- **M3** (open): Day 11's walker (Mira Dahl) washes at a Deck 4 basin until ~06:19 and never reaches Bunk 1, so the player standing there gets the 06:59 Mail with here:false.
  - (a) The walker must be in Bunk 1 by 06:30 with no other stop in between. In morning(), do the walk before wash/toilet, or wake them earlier (05:30 is already set: check the wash isn't put in between).
  - (b) A safety net in 24c: if you're in your bunk room from 06:30 and the walker hasn't come by 06:59, it still counts as attended (inspectRun(d, true)), never the "you weren't there" Mail.
- **S1:** the room lines b-h and inspect.walk.done are never heard. The WORK_TICKS line returns once inspectDue(d) is false, which is right after your result. Run inspectWalkTick for the whole walk, 06:30-07:20, outside the inspectDue guard.
- **S2:** anim 'look' isn't in ACTS, so the walker just stands. Use an anim that exists, or add it with section 8's owner.
- **S3:** add a live part to the check: the walker inside each room in order.
- **S4:** this note's older lines say STEP 3 / 06:29-06:54. It's STEP 5 now (06:30-07:10) and will change with M2.
Branch claude/inspection, head after this note. Tell lead 38 (session_01G2y9crUv6vDiiEB2q6Yo9W) and RV19 (session_01V6FDCQp5Ejidi8Chpo2nJG) when the fixes are in.
