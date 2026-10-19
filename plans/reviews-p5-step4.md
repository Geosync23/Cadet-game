# Reviews: Pillar 5 Step 3 last piece and Step 4 (reviewer R4)

R4 succeeds R3 (whose verdicts are in `plans/reviews-p5-step2.md`). Newest first.

## Playtest update 2 (brief: plans/brief-playtest2.md on claude/lead-pillar1; build master BM7 session_01QbuzvT3TwzMwSWRmakzX8Z)

### W2 claude/writer-p5 6a5d34a (0.48.104, the lines for items 1, 5, 9, 14, 15/20, 19): PASS
Lines skimmed. In a fresh archive content_gen bakes 9342 lines; lines_check PASS (0 errors, the 2 old "(Say nothing)" warnings). New placeholders `nth`, `start` are added to lines_check. `beam.congrats` is in both beam.lines (`@bank dept:works`) and the new beam-all.lines (`@bank all`): two different banks, so Works crew keep theirs and everyone else gets the new ones; not a clash. Torres's M1 meeting now explains rounds and sends you to the board (item 1). Builders, please note: `tip.round.look` says "Tap Look." (E1/U's button must be called Look), and `alarm.energy` shows a percentage, as item 5 asks.

## Step 4

### W2 claude/writer-p5 d1e62d3 (0.48.111, favour.call and favour.not for E2): PASS
Bakes 9564 lines; lines_check PASS. W2's tip.

### E3 claude/mech-diagnose 626a907 (0.53.6, M10 the workshop + tinkering, 24j): PASS WITH FIXES (two)
Diff from b8992d5b (E3's merge of E1 0.45.8). Line numbers below are in 626a907's starship-cadet.html. Read with a helper agent against m10-workshop.html; the two fixes were confirmed by hand.
- Good: posting matches the page (Day 12 Friday 08:00, then Mondays 08:00; seeded with keys 1010/1011 only, no R()). The board/lathe/fab places are E3's from 0.53.4. The steps are a 10-minute wait and a 2-minute hold. The first lesson goes through worksTeach('m10', ..., 'lead') = flag `train.m10.lead`, matching W2's lines. On hand-over: a friendship step, worksUse('m10'), +1 rep once a day through E1's worksSideXp. Lapse Mail after 7 days. All saved data under SHIP.works.side.shop. No new meshes. Ownership clean: ~30 new `shop*` / `SHOP_*` / `TINKER_*` names, none anywhere else; jobKindAdd and SOC_GIFTS are only called or appended to. The three hooks (jobTap, chatShow, chatDo) are typeof-guarded. `node --check` passes, and nothing it touches at load is defined later in the file (no TDZ).
- **Fix 1 (bug): an empty shelf skips the make.** shopFetch (~40729): with no part on the shelf it sets `j.parts = []`, then calls `jobStepDone(j.id, k)` with k counted before the fetch stop disappeared. Without that stop, k is the **make** stop, so the 10-minute lathe/fab wait is ticked off unmade. Tick the fetch step before clearing parts, or keep the part and let the make stop skip using it. Add a test with an empty shelf.
- **Fix 2 (the page): the thing goes into a hand.** The page: "The thing goes into a hand ... Hand it over in person (tap them)". In 0.53.6 the made thing never enters SHIP.player.carry; the hand-over is a chat button whether or not you have it. Put it in carry, and let the hand-over take it from there (or the lead accepts the shortcut).
- Notes (no fix asked): when nobody is acquainted a Works colleague asks (not on the page); the flag 'works.shop' is set but nothing reads it; 'shop' isn't in WORKS_SIDE_KINDS (harmless: finished with jobFinish, no turn-in note); shopData doesn't clean xpDay/taught/posted or an order's day/job/part (junk `taught` means the lesson is never given); mech_check has no real save round trip and its rep check accepts 0 or 1; the tinker time doesn't scale with needs, so the toast's "about N" can be off; from Day 6 the lathe/fab stop making GIFT_MAKES; any tap in main storage does the shop fetch; the 24k comment moved off its line at 35836/35837.
- Checks on 626a907: mech_check OK, social_check OK, cadet_test vs 7a6e137 ALL IDENTICAL.

### W2 claude/writer-p5 c058947 (0.48.110, five texts for E1): PASS
round.title.first, bench.charging ({time}), bench.charging.now, bench.rack, bench.rack.done; keys-p5.md updated. Bakes 9562 lines; lines_check PASS. W2's tip.

### W2 claude/writer-p5 7a5825b (0.48.109): PASS
works.order.lapse is a Mail body only; the tinker.* texts go (E3's WIP 2d90d7ec reads no tinker.* key). Bakes 9557 lines; lines_check PASS. W2's tip, contains 418b8c9.

### W2 claude/writer-p5 418b8c9 (0.48.108, M10 lines on E3's names): PASS
`works.order.ask.<id>` / `works.order.thanks.<id>` for E3's eight ids (guitar-hook ... tablet-stand, as in E3's WIP 2d90d7ec's order table) and `works.order.lapse`; the first lesson's crew lines move to Calder, Halloran and Torres under `flag:train.m10.lead` (E3's code must set that flag: checked at E3's M10 review). Bakes 9569 lines; lines_check PASS.

### E1 claude/mech-rounds b82c8e2 (0.45.10; contains 0.45.8 7a9a942 and 0.45.9 3d31f55): PASS
- **0.45.10, the fix for 0.45.7:** `toolUpkeepOn()` (the m11 row opened): `toolWear` adds wear only from then, `toolSlow` is 1 until then; mech_check's side part: 20 scans before M11 opens, still 100 and not slowed. Note: a save from 0.63.3 already carries the old wear (+.01 a scan, +.02 a use), which is still there when M11 opens; small, no fix asked.
- **0.45.8, ladder rows m10-m14 and m17** in 24 core's CAREER_LADDER table (inert until each sub-block registers WORK_MECH[id]). E2 also pushed m13/m14 behind `if (!ladderRow(...))`: the same values today, but two copies. E2 drops its pushes in 0.51.6 and asserts that E1's rows match its constants (ROW_AGREE), so E1's table is the one owner.
- **0.45.9, playtest 2 item 1, the rounds training:** `WORK_MECH.m1.self`: Torres's talk, then the whole training route is your job on the board (no teacher's round, no escort); `roundTrainStep()` (take / go / look / mark / next / done, with the machine's name, deck and place) is for U's arrow and green tips. mech_check M1_SELF walks it, twice the same. Notes: `round.title.first` has no line from W2 yet (the fallback reads fine); a save made mid-training on 0.63.3 keeps Torres's old two-stop round (a small window).
- Checks on b82c8e2: mech_check, career_check and machine_check OK; cadet_test vs 7a6e137 ALL IDENTICAL.

### E1 claude/mech-rounds b68e236 (0.45.7, round 1: 24 core tool wear, the side-job cap, Bunk 1 texts): PASS WITH FIXES (wear before Day 12)
Base 0.63.3 7a6e137. Pages: m11-tool-upkeep, step4-stages.
- One owner: toolWear/toolState/toolSlow/toolCharge, worksSide/worksSideXp/WORKS_SIDE_KINDS, myBedRoom/bedText are E1's alone. E2 (0df09137) and E3 (b809339) carry the base's one-line `const toolWear` untouched, so a merge takes E1's `function toolWear` cleanly. E2's `WORKS_SIDE_KINDS.add('leak')` (24o) comes after the core in the file. Good.
- Saves: `SHIP.works.side` kept whole by worksClean (< 64 KB, an object), an old save without it loads, junk dropped (mech_check side part). E1's keys: `side.slow` (the toast's day per tool), `side.xp` ({ day, n }). No R().
- Behaviour against m11: numbers as the page (4/5/3, Due < 30, Getting low < 60, a quarter slower, never blocked, toast once a day, words on the Tools page); worksUse no longer wears the three again. Cap +2 a ship day across side jobs; side kinds at the board go through it. WORK_BANDS[2] kept as C2's. Bunk 1 texts name the cabin after the move.
- **Fix: wear starts too early.** The page has M11 "from Day 12" ("Stage 1 · The scanner Day 12 on"; the pipe kit Day 12; the logger later). In 0.45.7 `scanRead` wears the scanner 4 a scan from the scanner's arrival (m7, Day 5), and `toolSlow` only looks at the charge: by Day 12 a busy player can have a Due scanner, slowing every inspection and toasting "Bench, when you can" before the bench lesson exists (and before 24m's bench upkeep is built at all). Gate it on M11 being open (Day 12 / the m11 ladder row): no wear before it (simplest: toolWear(id, n) only adds wear once M11 is open, so tools arrive at Day 12 charged), and a test line for it.
- Checks on b68e236: mech_check OK, career_check OK, cadet_test vs 7a6e137 ALL IDENTICAL.

### W2 claude/writer-p5 8879ee3 (0.48.106-107): PASS
tip.round.look no longer names a button; new `leak.worn` for E2 (in keys-p5.md). Bakes 9570 lines; lines_check PASS. Plus W2's handover note.

### W2 claude/writer-p5 b00e08b (0.48.105, Step 4 lines batch 1): PASS
Skimmed: step4.lines (414 lines), workshop.lines, five crew banks, ten training meetings (M11-M17). In a fresh archive content_gen bakes 9569 lines and 47 meetings; lines_check PASS (the 2 old warnings). No reputation numbers. M11 follows the lead's call (Halloran teaches "Torres's Friday routine" on Day 12; Torres's own version for when he's on shift).

### E3 claude/mech-diagnose b809339 (0.53.5, the leak joints moved): PASS
The five joints moved, same ids and order (3-leak-2 galley 35,3 'w'; 3-leak-4 promenade 23,9 'n'; 4-leak-2 starboard washroom 5,18 'e'; 4-leak-3 laundry 14,18 'e'; 4-leak-4 junior corridor 10,4 'n'), puddles with them. My edge probe on all 12: wall edge 'wall' or 'hull', place tile free, puddle tile free and in the same room. Screenshots look right. deck_check gains the line (leak tile free, wall edge wall/hull, puddle place free and in the room). Take this one, not 9d179e9.

### E3 claude/mech-diagnose 9d179e9 (0.53.4, the places turn): PASS WITH FIXES (five leak joints move)
Base 0.63.3 7a6e137. Diff: one places block after Step 3's, two Deck 5 props (your bench, the order board), build lines, DEV_NOTES.
- One owner: E3 alone defines `DECKS[n].leakJoints`, `growRacks`, `cabinSpots` and the new place ids; E2 (cfc4961a) only reads `leakJoints` through `placeById`. E1 (89369630) touches none of them. Good.
- Places are `type: 'event'` with `event: 'side' | 'leak' | 'leakp'`: inert for crew plans. Ids unique (deck_check OK, my run too). Nothing saved, no R().
- Props: the bench under the Works bay window (room w i0 10: the bench blocks tile 10,4; the place is 11,4, clear) and the order board on the machine shop's north wall (edges h,21-23,9 are 'wall'). Both look right in screenshots.
- **Fix: five leak joints are on the wrong spot.** I checked each joint's wall edge (EDGES at the place tile's `wall` side) and the place tile:
  - `3-leak-2` (galley 36,6 'w'): no edge at v,36,6, open floor: the joint and damp would hang in the air.
  - `3-leak-4` (promenade 13,9 'n'): the tile is BLOCKED by the call booths (12-14,9); standing there puts you inside the booth and the joint behind it. deck_check lets it through because a standing place on a blocked tile passes when a neighbour is reachable.
  - `4-leak-3` (laundry 12,16 'n') and `4-leak-4` (junior corridor 8,4 'n'): edge h,12,16 / h,8,4 is a `door`: the joint and damp would sit on a doorway.
  - `4-leak-2` (starboard washroom 2,18 's'): no edge at h,2,19: it's the curved hull, so the flat `wallAt` spot isn't on the wall.
  The other seven: wall or hull edges, tiles free, puddle tiles free and in the same room. Keep the ids and order (E2 reads them); move each to a free tile whose `wall` edge is 'wall' (or a straight 'hull'). Worth a line in deck_check: a leak place's tile free and its wall edge 'wall'/'hull'.
- Minor, no fix needed: `4-23-shelf` sits on exactly `4-23-keepsake`'s at/xy/face (fine while both are player-only).

## Step 3: U's Tracked device app

### U claude/hud-pt1 cf1348c (check only, on 1d602ff7): PASS
leave_check's reputation-chip test follows C2's careerJobIn: with the turn-in card (turnInShow) there's no floating chip, and the card's words are works.turnin.rep; without the card the old test runs. No game change.

### C2 claude/works-career f553607 (0.44.27): PASS (for BM6, over f3b744c)
One game line: careerJobIn pushes a department's rep entry into j.gains.rep only if none is there yet; plus build lines, career_check (calls it twice, expects one entry), C2's handover. No lines shared with U 1d602ff7.

### U claude/hud-pt1 1d602ff7 (0.72.4, button kept beside the app): PASS
Scope changed by the user ~04:00 (via lead 16): the device app stays AND the main-screen button stays. 94a1b127 below (button removed) is superseded, not to be merged.
- Merged on every Step 3 tip (as below), `node --check` clean. The button, panel, placement and frame loop are back as in 0.72.3 (the frame loop moved after recFrame, harmless); the panel and the app share `trkTap(key)` (true when it starts something: the panel or the device closes; a stop keeps it open and redraws). App first in the list, as below.
- turnInGains now shows one chip per department and one per system (the larger if a system shows twice). The doubled rep chip came from interactions_check seeding `j.gains.rep` before C2's careerJobIn pushed its own; in play C2 is the only writer of `g.rep`. C2's f553607 (0.44.27) also writes it once per department; the two guards agree (writer and reader), no shared names. Fine together; noted for one-owner hygiene only.
- Checks on the merge: interactions_check OK (5f6761e's job-by-title tap included), device_check OK, cadet_test vs the same merge without U's 0.72.4: ALL IDENTICAL, no state differences.

### U claude/hud-pt1 94a1b127 (0.72.4): PASS WITH FIXES (one check line, no game change)
Reviewed merged on every Step 3 tip (S2 0d0aa59, C2 f3b744c, M2 b3e5cf9, M3 42c76cc, H2 935b1d9, DA5 25dbfce, X 3a494c8, W2 a21487e; the jobStopsBase S2/H2 hunk resolved the known way, S2 first), `node --check` clean.
- Behaviour as asked: the HUD button, its panel, CSS, placement and frame loop all go; `deviceApp({ id: 'tracked', order: 1 })` is first in `deviceApps()` (boot -1 is hidden, home 0 is excluded, Settling in 5). The same `trkItems`/`trkOn` as before; a tap tracks (the device closes so the arrow shows), a second tap stops it (the device stays open); rows with no goal show "no arrow for this one" and aren't buttons. The heads-up's overlap list drops 'trkBtn'. Nothing saved.
- No other tip names trkBtn/trkPanel/trk* except interactions_check's old block, which is guarded by the button existing; no duplicate top-level names.
- cadet_test vs the same merge without 0.72.4: the only differing pixels are the old button's spot (x 132-254, y 86-115) in every shot; no state differences. device_check OK.
- interactions_check: **FAIL "a tap on your job tracks it again"** is the check, not the game: `tap('Job')` looked for the old panel's "Job" tag, which the app no longer shows on the job row (tags only on the "on" rows). With `tap(myJob().title)` the tap is found and the check passes. **Fix: in interactions_check.py, tap the job by its title** (e.g. `tap(g.ev('myJob().title'))`).
- The other FAIL (turn-in rep chip shown twice) is the known C2 f3b744c × U 0.72.3 clash BM6 is already placing; 0.72.4 doesn't touch the turn-in.
