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
about 9-10 h; each step reviewed as it arrives, every one on a phone-size screen.

### Step 1: bd558a84 (0.93.2-p.1, game sha256 0676819d...b1ef), PROMO_BEATS_ON true as pushed
Diff read: 24p's slot (PROMO_BEATS_ON, promoBeatsOn needs PROMO_SIGHT_ON too, PB_TIMES, promoBK, promoCerTimes,
promoCakeWin, promoBeatsApply mutating PROMO and OCCASIONS.promoSummons at load and each minute, promoBeatsPtr,
promoNotice, promoBeatsPassed, promoBeatsItems, promoBeatsWalkWait, promoTalkKind / promoTalkTick, promoBeatsTick, the
Torres onSim), 24p readers (promoPlan, promoScript, the summons and seek, the cake, the walk, promoCerDay / promoCerTick,
promoGuide's levels), section 19 (devDay rows; pointLimit's `force`), 15b (guideShift's test pointer), 25 (the steps
sorted), section 22 words (baked). Nothing new calls R() at load. Off: promoBK, promoCerTimes, promoCakeWin give PROMO's.

| Check | Build | Result |
|---|---|---|
| cadet_test vs b957b92d, alone | bd558a84, PROMO_BEATS_ON false | ALL IDENTICAL |
| cadet_test vs b957b92d, alone | bd558a84 as pushed (on) | ALL IDENTICAL |
| check_fast | bd558a84 | QUICK CHECK OK in 520 s |
| promo_beats_check, promo_sight_check, mech_check | bd558a84 | OK, OK, OK |
| career_check | bd558a84 | FAILED: 3. "busy: Relied on before Day 5" is old (b957b92d fails it too); NEW: "promoted once, on Day 10 at the scene: [[10, '10:00', 'mail']]" and "Tier 2 officer ... the reply remembered: None" (M3) |
| devmode_check | bd558a84 | FAILED (NEW): "the Day 10 promotion beat (at 08:02 the summons is booked, still a junior): clock Day 10 10:50, rank officer" (M4) |

### Played at phone size (390 x 844), Dev mode on a real Dev save (plans/rv19-promo-live.py)
Set career to Day 8, then the test morning, the board, the test turned in, the evening, the result day, the pip, the cabin.
- Day 8: the ready Mail and urgent notice at 06:00 ("Your Tier 2 test: tomorrow, 09:00"), Tomas's and Pell's luck Mails
  at 20:00. Good.
- Day 9 06:00 (in the bay): the morning notice; then Calder, as toasts because she isn't there, "There it is. Yours. I'm
  watching, not helping." (step3's promo.test.start, meant for 09:00) and "Morning. Nine o'clock it goes on the board" (S1).
  Tracked has "09:00 Your Tier 2 test". Bay chatter: "Your Tier 2 test? You've been aboard nine days." Good.
- Day 9 09:02, Teaching arrows Off, board open: the gold ring on the test's Take it, "Your Tier 2 test: take it" (shot
  B2). Good. (Another section's "Your shift starts now" banner sits over the list: not FX28's.)
- Turned in: Calder "That's the test. Filter in, fan settled.", the Mail and the urgent notice "Your result: tomorrow,
  08:15, the Chief's office"; the evening in the mess "Result tomorrow, first thing..." and "Heard you did your Tier 2
  test. How'd it go?". Good.
- Day 10 06:00: the result Mail and urgent notice; Tracked "08:15 Your result: the Chief's office". Good.
- Day 10 07:50-08:40, waiting in the Works bay (needs low, as after Dev skips): the only world arrow is a needs one,
  "Somewhere to sit and unwind" (shot D2); the office is marked only by Dev mode's own arrow. Calder never comes out: the
  meeting passes "missed" at about 08:45 with a "(notes)" Mail and the promotion by Mail (M1, M2). With needs topped up the
  result's arrow does show (shot G1) and walking into the office at 08:10 gives the promo.result card at 08:15; through
  it you're an Officer, the Captain's and friends' Mails, the invite "Your pip, 16:30". Good.
- Day 10 16:00: the urgent notice "The Captain pins your pip at 16:30... Go now." and Calder's word; the arrow from 16:10
  "Tap the lift: Deck 1 · Your commission" (shot H2). Good. Staying in the bay: 16:45 Calder's "The Captain's waiting"
  only as a toast (she's on Deck 1), the ceremony closes at 16:55 with a "(notes)" Mail (S2), and at 19:28 (in a Dev
  skip) the commission-by-Mail says "Your commission, 17:15 | The officer ceremony is today at 17:15..." (S3).
- 20:00 (never ate): the urgent notice "Calder is walking you there now", her lines as toasts; at 20:30 not walked yet,
  still the bunk (she has to come from wherever she is; S4).
- Dev mode note: a Dev clock skip past 12:30 on the result day "excuses" it, which moves the result to the next workday
  while the "(notes)" Mail already says you passed. Dev only.

### Findings
**Must**
- M1. The result's arrow (promoGuide's promo:summons) is level 2; an urgent needs nudge took the world arrow all of 07:50
  -08:40 in my run. Make it level 1, like the test's, the pip's and the cabin's: the step the user most wants unmissable.
- M2. In the Works bay at 08:15 (the likeliest place: you clock in there; the office is in the bay) nothing happens: the
  seek skips `promoInBay()`, so the result goes by Mail at about 08:45. With the switch on, Calder should come out to you in
  the bay too (or the card start beside her door), so the result is always said in person unless you're nowhere near.
- M3. career_check fails twice where 0.93.1 passes: the promotion comes by Mail at 10:00, not at the scene, and the reply
  isn't remembered. Fix the cause or the check, and say which.
- M4. devmode_check fails: Dev mode's Day 10 promotion beat (DM_BEATS 'promo') still lands at 10:50, after the 08:15 result,
  so you're already an Officer. Move it to the new time with the switch on.

**Should**
- S1. On the test morning Calder's step3 line "There it is. Yours. I'm watching, not helping." comes at 06:00 (the job is
  made then, found at 09:00), before her new morning word; both as toasts when she isn't there. Say "There it is" when the
  job is up, and the morning word only when she's in the bay with you (worksSay toasts otherwise). Check 0.93.1 too.
- S2. The pip's seek: r.len is stretched to hold the room, but the ceremony closed at 16:55 (+25) without you, and Calder
  never reached the bay from Deck 1. Check the room waits as meant, switch off and on.
- S3. promoCommission's Mail uses `mail.promo.ceremony`, an invite text with "17:15" (content/works/step3.lines): wrong
  words for a missed commission, and with the switch on the wrong time too. (Off: the same words exist in 0.93.1; a
  backlog row if not fixed here.)
- S4. The 20:00 walk says "Calder is walking you there now" while she's elsewhere; her lines arrive as toasts and nothing
  had happened by 20:30. Have her come to you first, or word it as "Calder's on her way".
- S5. The two build-number lines are the build master's (0.93.2-p.1 here).
- S6. "Works reputation down: New officer" shows twice the afternoon you're promoted (xp reset to 0). Reads as a
  punishment on your best day. Probably old; worth a word or a backlog row.

**Verdict on bd558a84: FIXES NEEDED (M1-M4).**

### Step 1b: 104420fd (game sha256 6f975a4d...dc288; sent at 07:32, before my verdict on bd558a84)
Since bd558a84: SW2's word polish (promo.result's opening and lines, promo-beats banks), Dev mode's promotion beat at 08:05
with the switch on (DM_BEATS 'promo' `at` getter), career_check meets the 08:15 result between its hourly steps, backlog
FX28-1. Checks: cadet_test vs b957b92d with the switch off ALL IDENTICAL; career_check only the known-old "busy: Relied on
before Day 5" (M3 done); devmode_check OK (M4 done). M1 (the result's arrow level 2) and M2 (no seek in the Works bay) are
unchanged in the code (promoGuide, promoSummonsTick), so the live finding stands.

**Verdict on 104420fd: FIXES NEEDED (M1, M2; S1-S6 as above).**

### Step 2: 44a4565f (game sha256 e88aadfe...3575)
Diff read (vs 104420fd): promo:summons level 1 with the switch on (M1); the summons seek checks the office
(promoInOffice), not the bay, with the switch on (M2); "There it is. Yours." held to 09:00 when the test is made earlier,
once (flag pb.tell; S1); the missed commission's Mail through promoBK to promo.ceremony.mail (S3); the evening walk's
escort follows you first, then leads once she's within 2.5 tiles or 15 minutes on, W.mv.met, the notice and her word
reworded (S4); promo.move.notice through promoBK. Off: every change is behind promoBeatsOn().

| Check | Build | Result |
|---|---|---|
| cadet_test vs b957b92d, alone | 44a4565f, PROMO_BEATS_ON false | ALL IDENTICAL (renderer noise only) |
| career_check | 44a4565f | only the known-old "busy: Relied on before Day 5" (backlog FX28-1) |
| promo_beats_check | 44a4565f | PROMO BEATS CHECK OK (new part `review`) |
| check_fast, devmode_check, lines_check, names_check | 44a4565f | OK (FX28's runs) |

Played again at 390 x 844 (plans/rv19-promo-live.py, the player left waiting in the Works bay, needs low, no top-up):
- 08:20: the world arrow "Your result: the Chief's office, 08:15" and the banner "Your result: the Chief's office is
  starting · Go there", over the hunger and shower nudges (M1 fixed).
- 08:32: Calder comes out to you: "There you are. My office was the plan. Here will do.", then the promo.result card where
  you stand, readable at phone size; through it you're an Officer, the Captain's and friends' Mails (M2 fixed).
- Missed pip: the Mail now reads "We missed you at the ceremony, so the Captain signed it anyway..." (S3 fixed).
- 20:00: "Chief Ines Calder is coming to find you and take you there."; at 20:03 she reaches you in the bay: "There you
  are. Your cabin, then. With me." (S4 fixed; the walk itself needs you to follow her, so my standing probe stops there).

Accepted, no change: S2 (the pip's seek at +15 and the room closing at its length, as 0.93.1 does), S5 (lead 38 asked
FX28 to set 0.93.2-p.1), S6 (the "New officer" reputation toast comes from xp resetting at promotion, as before).
Note N1: in my run the result card took about 30 ship minutes (my probe's slow taps), so section 18 also sent a
"(notes)" Mail at 08:45 while the card was still open; at a normal reading pace the card ends well before.

**Verdict on 44a4565f: PASS.**

## FX26, Storm Saturday (claude/storm-sat), from RV18's queue (agreed with RV18 and lead 38, 08:40)
Final: 402899bd (0.93.2-w.5, game sha256 c799f15eeccbe7f1...7cd). Steps: w.1 7091043 (the Captain's stage fix, not switched;
the call-in, storm-only board, Calder's Mail behind STORM_SAT_ON; leave_check's day off moved to Day 14), w.2 ea0ace07
(the lantern supper is that day's dinner; Storm stories by torchlight), w.3 41d891b9 (lanterns and low light), w.4
67e918f2 (the stories said aloud, a seat kept for you, Oduya's close, chatter hushed), 4774b7f1 (section 15's actEnd: a
joinable tradition's end toast titled with its name, not its id, for every tradition), w.5 402899bd (the supper's sittings
35-50 min so nobody eats standing). STORM_SAT_ON = EV_STORM_ON, so it is on as pushed; "off" = a copy with it false.
Lead calls already made: a missed call-in costs reputation like a missed shift but not toward being let go; repairs count
to the commendation; not a double; leave_check's sample day 13 -> 14.

Diff read: section 18's slot 'Storm Saturday' (stormSatDay from the calendar plan and the storm's phases only, cached;
stormCalledIn, playerCalledIn, playerOnDuty, stormBoardJob / stormBoardHide; stormSay / stormStoriesFrame), the storm's
`if (STORM_SAT_ON)` block (seven storm repairs in three waves, the Mail, S.stormSat, dayDress, keep, stayIn's gap, the
supper for everyone, the dressing, TRAD_JOIN), section 14's isWorkDay (+ stormCalledIn), playerShiftOn -> playerOnDuty in
13, 15, 15b, 19, 20, 25 (time clock, arrows, tea, Schedule, alarms), the board's filters (15b, 17), devDay's row and no
second dinner, DECK_DRESS.stormTorches and stormSupperDim, the rec deck's floorY and 8b's CrowdPerson fy and bubbles'
stage height, the storm-stories tradition (content/traditions/storm-stories.trad). Nothing new calls R() at load.

| Check | Build | Where | Result |
|---|---|---|---|
| cadet_test vs b957b92d, alone | 402899bd, STORM_SAT_ON false | RV19 | ALL IDENTICAL |
| cadet_test vs b957b92d, alone | 402899bd as pushed | RV19 | ALL IDENTICAL |
| check_fast | 402899bd | FX26 (and 41d891b9 RV19) | QUICK CHECK OK |
| day_check 12, 13, 14 | 402899bd | RV19 | DAY CHECK OK, all three; schedules 0/0/0/0/0 |
| weekend_check, player_check | 402899bd | RV19 | OK, OK |
| career_check | 402899bd | RV19 | only the known-old "busy: Relied on before Day 5" (backlog FX28-1) |
| events_check, join_check (alone), devmode_check, bigevents_check | 402899bd | CR5 | all OK |
| fridays_check, arrows_check | 402899bd | CR6 | FRIDAYS CHECK OK, ARROWS CHECK OK |
| events_check, devmode_check, day_check 13 | 41d891b9 | RV19 | OK |

Played at 390 x 844 (plans/rv19-storm-live.py, Dev mode on a Dev save):
- Friday Day 12, 18:00: Calder's "You're needed tomorrow" Mail and Oduya's invite to the storm stories.
- Saturday Day 13: the Schedule "09:00 On shift: called in for storm repairs"; the board (shot): only "Storm repair: ..."
  jobs, plus two power jobs the crew already hold; 4 other jobs hidden; at 10:00, 15 of 18 Works day crew at work.
- 18:00 the lantern supper on the Schedule, no second dinner; in the mess "You squeeze in at a long table in the lamp light".
- 21:05 the storm stories (67e918f2 and 402899bd): tap Oduya, you sit in the circle in the junior common room (no longer
  walked out to the corridor, as RV18 and I saw on 41d891b9); the room dark with the lanterns on the rug (shot); the
  tellers' storms in turn ("Hailstones the size of eggs on the farm moon..."), the asides, Oduya's prompts, his close at
  21:36 and 21:38; no page errors. Meets the user's rule: a host to tap, a pose, its own words.
- Not checked by me: the Captain's stage fix (RV18 played it: standing on the stage, the bubble above her head).

Notes (not blocking):
- N1. The asides rotate over four lines: "And then the window just... went" came 3 times in 30 minutes.
- N2. The join toast shows twice (once on the tap, once as the activity starts) and its "About N minutes" ignores a late
  join; FX26 says every joinable tradition does this (old).
- N3. 4774b7f1 changes section 15's actEnd (the player engineer's) for every joinable tradition's end toast: worth the
  owner's look at merge time; join_check and player_check are OK on it.
- N4. stormSatDay is cached the first time it's asked (STORM_SAT_D) and a Saturday only; a calendar that moves the storm
  within one page (a new game without a reload) would keep the old day. New game reloads today, so no effect.

**Verdict on 402899bd: PASS.**

### Storm Saturday follow-up: 6f19944d (0.93.2-w.6, game sha256 1eb61da940e735a4...)
BM18's mech_check m9 FAIL (lead 38: fix in the game): stormBoardMine(j) (held by you, train, case, symptom, reserved,
heldForYou, or SHIP.works.cur.j); stormBoardHide now also needs !stormBoardMine, so the storm Saturday's board only hides
unclaimed ordinary jobs and never your own work. Only that function changed (plus docs and FX26's handover note).
Checks (RV19): cadet_test vs b957b92d with STORM_SAT_ON false ALL IDENTICAL (renderer noise only); mech_check MECH CHECK
OK; day_check 13 DAY CHECK OK. FX26: check_fast OK, cadet_test off/on identical.

**Verdict on 6f19944d: PASS.**

### Save slots, test-only follow-up: a1df5739 (saves_check.py only; game unchanged, d7b6a9f4...2e09)
Since ba6b7b9a: longer waits (load 120 s, cards, picker, download 60 s), a stopped part prints its traceback, builds and
links switched in the same tab, a diagnostic line if the old save is missing, and the game served from
http://saves-check.test/ by a Playwright route (the same file) instead of file:// (FX27 measured a navigated file:// page
now and then handed a fresh empty storage, with the slots-off build too: a check problem, not the game). The checks still
check the same things; one web origin is how a player meets the game (RV19's own slots check used an http server too).
RV19: game sha256 confirmed unchanged; saves_check (all parts) SAVES CHECK OK; migrate alone 6 of 6 OK.

**Verdict on a1df5739: PASS (test only).**

## B1, Pillar 5 Step 5 skeleton (S5-1 turn 1): claude/p5s5-skeleton 5957d244 (game commit 2d679a85, sha256 97e104ed...63df; from d9c7e5f0)
For lead 39, against plans/p5-step5-spec.html (claude/p5-specs db1313c1). I review section 18 for the events seat.
Switch: `P5_STEP5 = URL_FLAGS.has('p5s5')` (off unless ?p5s5; "on" runs use a copy with `const P5_STEP5 = true;`).

Diff read: section 13's six switch lines; section 18's `if (P5_STEP5)` block after the swap's (EV_BEATS); section 24
core's `if (P5_STEP5)` block (nine ladder rows, WORK_TOOLS.arrayrig, WORK_BANDS[3] a copy of tier 2's); empty sections
24u-24x with slots; owners.md, map.md, affected.py RULES, DEV_NOTES. Nothing calls R() at load.
- EV_BEATS against the spec's section 4 table, row by row: tier3Test Day 15 09:00-15:00; seniorResult (new) Day 16
  08:15-08:30; seniorOfficer Day 16 16:15-17:30; nightAssigned Day 22 09:15-09:30; nightShift1 Day 22 22:40-06:00;
  nightShift2 Day 23 20:45-06:00; nightShift3 (new) Day 24 20:45-06:00; engineSpecialist Day 23 16:15-17:10 (kind
  captain, as the table); caldersQuestion Day 26 18:40-19:30; seniorToast, shutdownsTraining, mondayBriefing untouched.
  All match. Off: the block doesn't run, nothing moves.
- Ladder rows inert: ladderTick only opens a row with WORK_MECH[r.id] registered, and none of the nine has one yet.
- Job slots: the existing big rows are m1, m4, m5, m7, m6, t2, m8, m9, m15, m17 (slots 10-19); the new t3, m19, m18, m20
  wrap to 10-13, m1/m4/m5/m7's. A clash needs both reserved at once (those four are first-week trainings), and B1's
  handover and DEV_NOTES tell builders to reserve their own slot (20 is the Tier 2 test's, 24 the fix-scan's).

| Check | Build | Result |
|---|---|---|
| cadet_test vs d9c7e5f0, alone | 5957d244 (off) | ALL IDENTICAL |
| check_fast | 5957d244 | QUICK CHECK OK in 353 s |
| bigevents_check | 5957d244 off | BIGEVENTS CHECK OK |
| events_check | P5_STEP5 on copy | FAILED only on the known-old FX24-2 (farouk-olu, reading corner Day 7; accepted for 0.93.2) |
| bigevents_check | P5_STEP5 on copy | FAILED: "the guard's samples [False, True, True, True, True, False] (want: test Day 15 no; Day 18 16:00 yes; Day 20 19:30-21:00 no; 19:00-20:15 yes; the night shift Day 21 05:00 no; Friday 16:00 no)" |

### Findings
**Must**
- M1 (check only). bigevents_check fails with P5_STEP5 on: its guard samples still expect the old hours (the night
  shifts on Days 19-21, so "Day 20 19:30-21:00 no" and "Day 21 05:00 no"). With v3.1 those hours are free (the
  spec: the Captain's table back to 19:30 on Day 20; nights on Days 22-24), so the guard is right and the check is
  stale. Give the check v3.1 samples when P5_STEP5 is on (e.g. Day 15 09:00-15:00 no, Day 16 08:15 and 16:30 no,
  Day 22 23:00 no, Day 24 21:00 no, Day 20 19:30 yes), keep today's samples when it's off, and run it both ways.
  bigevents_check is EC1's: agree the change with its owner. The game itself is right.

**Should**
- S1. The spec's S5-1 checks list day_check's EVENT_DAYS 15 and 16 and career/mech parts: fine for turns 2-3, as B1's
  handover says; keep them on the list.

**Verdict on 5957d244: FIXES NEEDED (M1, a check change only; the game skeleton is right and off is identical).** If
lead 39 wants the skeleton merged now to unblock S5-2..S5-6, it is safe with the switch off; M1 then belongs to turn 2.
