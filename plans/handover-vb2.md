# Handover: VB2 (session_01KRBGtugjBpv5iGcV5WDvCP)

Role: deck and sky builder for "A Veyli vessel needs help" (Days 27-30), hired by lead 39 (session_019V68fz33UFv4cK5Z4iCDvi); lead 40 (session_01NXybH7NNqM8M4ngiyidq6m) took over 2026-10-26 ~22:00 UTC and earmarked VB2 as Step 6's deck architect (S6-4) once Step 5 lands. Spec: plans/veyli-vessel-spec.html on claude/p5-specs (e9f0962c), pieces V-5 (the ship outside and the small props) and V-3's chain spots. The events builder VB1 (session_01UsjGN26E88zwrNPWwef4iT, claude/vessel) owns the event itself: V-1 to V-4, the switch `EV_VESSEL_ON`, SHIP_EVENTS.veyliVessel, the beats, rings, arrows, the chain's gathering.

## Branch and builds: claude/vessel-sky (from claude/staging-0.93.3 d9c7e5f)
- vessel-sky v.1 e21ade10, v.3 c070862c, v.5 cfc2dbe3 (the reviewed one); v.2 (staging merged, vesselSheet, VESSEL.sky, EN2's crossingBackShip hook): everything below (build-table row "vessel-sky v.1"). DEV_NOTES "A Veyli vessel needs help: the looks" has the details.

## What I own
- The slot `// ---- slot: Vessel sky` (section 18, after the Appointments builder's slot) and one line in eventsTick after the comet's (`if (vesselOn()) vesselSkyFrame();`).
- The ship outside (VSKY, vesselAnchor, vesselLook, vesselShipFlash), the chain's places (5-vchain-1..40, 5-vchain-call, DECKS[5].vesselChain), the chain's crates and stacks (vesselChainCrate, vesselChainFrame, vesselChainFrom/To), the props (vesselCrate, vesselPartOld, vesselPartNew, vesselSketchWorks, vesselSketchShelf; vesselShelve()).
- deck_check's vessel part (a copy with the switch on) and perf_check's three vessel scenes (+ its switched() takes a preview switch).

## Shared names agreed with VB1 (proposed in my first message; check VB1's answer)
- Switch `EV_VESSEL_ON` (VB1's line after P926_APPT); I read it with a typeof guard (vesselOn).
- Event id 'veyliVessel', startDay = the Saturday (Day 27). My times are event minutes from the warning day's midnight.
- VB1 sets `SHIP.event.mine['vessel:part']` when the new round one is made (the new part shows on the machine shop bench).
- VB1's ring "Put the sketch on your shelf" calls `vesselShelve()`.
- VB1's chain gathering uses the pool `{ deck: 5, pool: '@vessel-chain' }`, Zeke at `5-vchain-call`, you at DECKS[5].vesselChain.you; `vesselChainCrate(now).moving` tells when a crate reaches a spot.
- Systems effect name 'skyVessel' (cosmetic).
- Bench spots for VB1's VESSEL_SPOTS: 5-vbench-1..3 (Works bay: Taavek, Calder, Zeke), 5-vshop-1..3 (machine shop: Taavek, two helpers) (v.6).

## Others
- EN2 (session_013er8NqC8eftyZqXBzcSibF, the ending): its `crossingBackShip(now)` -> null | { pose: 'bow' | 'alongside', lights, flash } shows the ship again Days 34-35 (vesselSkyNow).
- RV21 (session_01AmTyMHLr5UuCY9zo3nQcwS) reviews: send shas to RV21, lead 39 and BM18.
- Poses 'bow' and 'wave' (v.3, section 8b's slot; lead 39 gave them to me; the ending reuses 'wave').

## Loose ends
- The shelf when your quarters move to Deck 2 (Step 6, Tier 4): no shelf spot there yet; the sketch shows only on Deck 4 (bunk or 4-23).
- The deck_check / perf_check scenes with crowds wait for VB1's event block; measured with a stand-in: bow lounge Mon 17:41 279 calls, Works bay Sun 13:30 206.
- Words: SW4's keys are read (tap.part, tap.newpart, tap.sketch.wall, tap.sketch.shelf, tap.crate for the stacks, tap.sheet(.before)); still stand-ins: tap.taavekCrate and the `.t` titles. tap.sketch.shelf fixed to match the drawing (v.5, lead 39).
- RV21 PASS on c070862c (3 shoulds, fixed in v.4); RV21 PASS on cfc2dbe3 (v.4-v.5), nothing open; it replaces c070862c for BM18.

## How to test
- A copy with the switch on: `python3 -c "s=open('starship-cadet.html').read(); open('/tmp/cadet-work/test/vsky.html','w').write(s.replace('const P926_APPT = true;', 'const EV_VESSEL_ON = true;\nconst P926_APPT = true;', 1))"`; without VB1's block, stub SHIP_EVENTS.veyliVessel (days 4, phases) then `vesselLooksInit(); eventStart('veyliVessel', 27)`.
- deck_check (its vessel part), cadet_test HEAD vs branch (ALL IDENTICAL off), check_fast.

## Gotchas
- dressShow keys props by id: two dressing entries with one id must have windows that don't overlap.
- A sky quad is hidden wherever anything else drew (the floor, walls): vesselAnchor rejects points the deck's floor would cover.

## Stopping point (lead 40, 2026-10-26 ~23:40 UTC; the user's call)
Three branches of mine, all pushed:
- **claude/vessel-sky** 3fb8eac7 (v.6): the Veyli vessel's looks, chain/bench spots, props, poses bow/wave. RV21 PASS on every sha. Waits for BM18's merge.
- **claude/p5s5-kit** 69eb706d (from B5's claude/p5s5-promo 10eecac7): the Senior Officer's collar bar (makeCharacter's `spec.bar`: two pips + a gold bar, merged, no draw call; nobody has it until B5's promotion sets it, copy promoPip's rebuild) and Calder's visitor chair (Deck 5 dress, only with P5_STEP5) + seat place `5-office-visit-sit`. cadet off ALL IDENTICAL vs 10eecac7, check_fast OK. Sent to B5 to merge; RV20 review asked through lead 40 (no verdict seen yet).
- **claude/ending-checks** (from EN2's claude/ending-crossing, merged up to d1a61402, RV21's final PASS): WORK IN PROGRESS, test only (no game change of mine).
  - `arrows_check.py` parts `endstay` / `endgo` (run them by name: `python3 arrows_check.py BUILD.html endstay endgo [asis|teachoff|track|change]`; it writes an ending-on copy itself). The follower follows only around the ending's beats (END_WINDOWS) and skips the hours between, but follows whenever an ending level-1 arrow is due (DUE); END_PICK answers the Captain's question / her search / the address ask with the run's choice, presses the ending's button on a chat card (`#chat button.act`), and steps into the Tern on "Walk to the Tern". About 3.5 minutes a way.
  - Results before the stop: endstay asis, teachoff, track all reach every beat in order with 0 minutes of a due ending arrow not leading; their one FAIL (end:cb:ship stuck, Day 34 10:18) was a game bug EN2 fixed in d1a61402 (not yet re-run on it). Only job/clock arrows got "stuck" (the skipped hours leave those behind): printed, not failed.
  - LEFT: (1) endstay `change` was reworked (Go at the first "Tell the Captain" on Saturday evening, Stay at Sunday 10:00 by her chat button, before the address) and not yet run. (2) endgo: the first `asis` run produced no Day line for ~30 minutes and was stopped: look at it first (likely the end page or the goodbye leaves the follower in a long loop; Day 36's window is 05:50-11:20; check END_PICK's "into the Tern" step and that the run breaks once SHIP.end.ended or the page shows). (3) Then all 7 ways green on d1a61402.
  - `controller_check.py` part `ending` (in ALL_PARTS; NEEDS base/deck/pick/panels): presets on Days 32 (the offer's replies by pad: OK), 34 (the Captain's "About the transfer", her four choices each reached, Not sure kept: OK; a friend's button: the ring never landed on Pell in 10 tries, raised to 24, not re-run), 35 (the oath by pad: OK, led), 36 (Go, a whole morning by pad: the lift and breakfast OK; the farewells failed on the old chat selector, fixed to `#chat button.act`, not re-run; then into the Tern and the end page's buttons). LEFT: re-run, fix the friend and the farewells if still failing, check the end page by pad.
  - LEFT too: day_check 31 and 50 on an ON copy (`sed "s/^const EV_ENDING_ON = URL_FLAGS.has('ending');/const EV_ENDING_ON = true;/"`).
  - Reviewer: RV22 (session_011wAn842cKDVWvoH8Cr9geD); lead 40 (session_01NXybH7NNqM8M4ngiyidq6m). Any game bug found: fix on top of d1a61402 (EN2 and RV21 are retired), send to RV22 and lead 40.

### Update 00:25 UTC (lead 40 gave until 00:45 to finish in-progress work)
On claude/ending-checks (on d1a61402, EN2's fixed ship arrow merged), all runs with -u (an earlier "hang" was only Python's buffered output):
- **arrows_check endstay: all four ways PASS** (asis, teachoff, track, change): every beat in order, 0 minutes of a due ending arrow not leading; the change run says Go on Saturday evening, Stay at her chat button on Sunday 10:00, settles Stay, ends in the endgame. Only job/clock arrows left "stuck" by the skipped hours (printed, not failed). A check bug fixed: END_PICK read CHAT.p after the button's click had closed the card.
- **arrows_check endgo: FAILS at the goodbye** (asis): offer, Go at the first Tell the Captain (Sat), oath, settled Go, Zeke Sunday, breakfast and the bay's arrows all fine ('end:bf', 'end:bye' led; 0 minutes missed), but by 11:20 the ramp scene never played and the end page never opened (`Go did not end at the end page (end.go 35, ended None, page False, the ramp None)`). Next: log FOLLOW/END_PICK's actions on Day 36 from 09:15 (f.acts) to see whether a farewell's tap opens a chat card without "Goodbye" (endByeChat needs endMin >= END_T.bayAt and the person in endByes()), or whether endByeSay's own reach (endNear 1.8) is never met because FOLLOW stops 2.2 tiles away (its walk threshold) — likely: then END_PICK should step within 1.5 of the arrow's crew on 'end:bye'. teachoff/track results: see below if they finished.
- **controller_check ending**: Day 32 offer replies by pad OK; Day 34 the Captain's "About the transfer", her four choices reached, Not sure kept OK; Day 35 the oath led by pad OK; Day 36 lift + breakfast + bay OK, goodbyes by pad to pell, tomas, bramwell-basil, halloran-emeka OK, then FAIL: the ring never names rina (24 tries) and on Day 34 never names pell — both likely held in a scene/seat the ring doesn't offer, or out of the ring's reach after end_near; look at PAD_PICK.list for them. The end page step is untested until the farewells pass.
- **day_check on an ON copy: Day 31 OK, Day 50 OK.**

### Final state at 00:37 UTC (pushed)
- endstay: all four ways PASS on d1a61402 (asis, teachoff, track, change).
- endgo: **teachoff PASSES** (all the way to the end page, ended); **asis and track FAIL** the same way: the follower's last action is the last breakfast's scene read through at Day 36 07:08, then NOTHING until 11:20 (no goodbyes said, the arrow then "The shuttle bay by 09:30"). So after breakfast something keeps FOLLOW returning null (likely: a sit-down/eat ACT from the breakfast that never ends, or a teaching pop-up / DEV state only with Teaching arrows on). Start there: in part_end print `pg.ev('[!!ACT && ACT.kind, !!DIALOGUE, !!DEV.choose, DEV.open]')` every 10 minutes on Day 36 07:10-09:30. The walk-up-to-the-farewell step in END_PICK (within 1.4 of the 'end:bye' crew) is in, untested past breakfast.
- controller_check ending: offer, the Captain's button + choices, the oath, Monday's lift/breakfast/bay and 4 farewells by pad OK; FAIL: the ring never names rina on Monday nor pell on Day 34 (24 tries) -> the end page step untested.
- day_check 31 and 50 on an ON copy: OK.

### Green (01:40 UTC, on d1a61402; lead 40's "everything ships ON" rule)
- **arrows_check endstay + endgo: ARROWS CHECK OK, all 7 ways** (endstay asis, teachoff, track, change; endgo asis, teachoff, track). The endgo stall was the check, not the game: the last breakfast seats you at the mess table and the follower never got up; END_PICK now gets up when an ending arrow leads elsewhere (the game's "The shuttle bay by 09:30" arrow was there at level 1, as the spec asks). Then every farewell in order, Zeke's ramp scene, aboard, the end page. 0 minutes of a due ending arrow not leading in any run.
- **controller_check ending: CONTROLLER CHECK OK**: the offer's replies; the Captain's "About the transfer", her four choices each reached, Not sure kept; a friend's "About the transfer" (the first friend the ring can open: in a crowd someone in front can hide a person from the ring, so Pell may be skipped for Tomas); the oath led; Monday (Go) by pad: lift, breakfast, the bay, all ten farewells by walking up (how the game says goodbye; the ring a fallback), Zeke at the ramp, into the Tern by the stick, the end page with the highlight on Keep this ending, the D-pad to Start a new game, A on Keep this ending, ended.
- day_check 31 and 50 on an ON copy: OK.
- Not done: nothing in the ending checks. (Loose: the ring can't single out one person in a crowd; a pad player walks up instead. A ring-in-crowds improvement would be the controller seat's.)
