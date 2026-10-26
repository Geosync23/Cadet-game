# Handover: VB2 (session_01KRBGtugjBpv5iGcV5WDvCP)

Role: deck and sky builder for "A Veyli vessel needs help" (Days 27-30), hired by lead 39 (session_019V68fz33UFv4cK5Z4iCDvi). Spec: plans/veyli-vessel-spec.html on claude/p5-specs (e9f0962c), pieces V-5 (the ship outside and the small props) and V-3's chain spots. The events builder VB1 (session_01UsjGN26E88zwrNPWwef4iT, claude/vessel) owns the event itself: V-1 to V-4, the switch `EV_VESSEL_ON`, SHIP_EVENTS.veyliVessel, the beats, rings, arrows, the chain's gathering.

## Branch and builds: claude/vessel-sky (from claude/staging-0.93.3 d9c7e5f)
- vessel-sky v.1 e21ade10, v.2 (staging merged, vesselSheet, VESSEL.sky, EN2's crossingBackShip hook): everything below (build-table row "vessel-sky v.1"). DEV_NOTES "A Veyli vessel needs help: the looks" has the details.

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

## Others
- EN2 (session_013er8NqC8eftyZqXBzcSibF, the ending): its `crossingBackShip(now)` -> null | { pose: 'bow' | 'alongside', lights, flash } shows the ship again Days 34-35 (vesselSkyNow).
- RV21 (session_01AmTyMHLr5UuCY9zo3nQcwS) reviews: send shas to RV21, lead 39 and BM18.
- Poses 'bow' and 'wave' (v.3, section 8b's slot; lead 39 gave them to me; the ending reuses 'wave').

## Loose ends
- The shelf when your quarters move to Deck 2 (Step 6, Tier 4): no shelf spot there yet; the sketch shows only on Deck 4 (bunk or 4-23).
- The deck_check / perf_check scenes with crowds wait for VB1's event block; measured with a stand-in: bow lounge Mon 17:41 279 calls, Works bay Sun 13:30 206.
- Words: SW4's keys are read (tap.part, tap.newpart, tap.sketch.wall, tap.sketch.shelf, tap.crate for the stacks, tap.sheet(.before)); still stand-ins: tap.taavekCrate and the `.t` titles. tap.sketch.shelf fixed to match the drawing (v.5, lead 39).
- RV21 PASS on c070862c (3 shoulds, fixed in v.4).

## How to test
- A copy with the switch on: `python3 -c "s=open('starship-cadet.html').read(); open('/tmp/cadet-work/test/vsky.html','w').write(s.replace('const P926_APPT = true;', 'const EV_VESSEL_ON = true;\nconst P926_APPT = true;', 1))"`; without VB1's block, stub SHIP_EVENTS.veyliVessel (days 4, phases) then `vesselLooksInit(); eventStart('veyliVessel', 27)`.
- deck_check (its vessel part), cadet_test HEAD vs branch (ALL IDENTICAL off), check_fast.

## Gotchas
- dressShow keys props by id: two dressing entries with one id must have windows that don't overlap.
- A sky quad is hidden wherever anything else drew (the floor, walls): vesselAnchor rejects points the deck's floor would cover.
