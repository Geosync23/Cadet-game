# Handover: FX7 (fixes and find-the-cause jobs under lead 31), 2026-10-23

Role: a helper under lead 31 (session_0118SXBCdg87nDiXdtrGNVSR). Each job came from the lead, on its own branch, with a
row in plans/build-table.md under its own heading. Reviewer: RV10 (session_01XeJ6bvySekD1V8Sfh1tzgb), except
floor-tap-fix (FX4). Build masters: BM14 (0.92.0), BM15 (0.92.1, 0.92.2: session_01EH5qkoYriK2Gsrp7hHRoso).
Nothing here sets build numbers.

## Branches and state (all pushed; every check named below was run before each push)
| Branch | Base | Tip | What | Review |
|---|---|---|---|---|
| claude/tiles-sit | breakfast-back 0cd37b1b | 0a58748e | The Tiles partner sits at the board you tapped: `tilesBoardSeats` (section 23) uses the deck's own seat lists (DECKS[n].tiles), not every seat within 2.4 m; someone already walking to a stool plays you | RV10 PASS, in 0.92.0 |
| claude/floor-tap-fix | integration-next-fe1 01b237f4 | aaab3540 | A floor tap by an exercise bike threw `updateWorldMatrix` (ixTap measured a hit-less stand-in); ixTap now measures a stand-in from the spot tapped (section 15b) | FX4 PASS, in 0.92.0 |
| claude/tiles-check-queue | integration-next 25a90ced | 664e0baa | tiles_check: SHOW_ALL once after load (the arrows' pop-up queue), test only | sent to BM14 |
| claude/bike-tap | integration 685af944 | 9328dc76 | LEAD31-1: playerFloorTap takes the place right where the floor was tapped first; both bikes have a saddle-high tap box | RV10 PASS, for 0.92.1 |
| claude/mess-taps | integration-next 54efee21 | 980c2591 | LEAD31-9: a second tap on your seat mid-meal keeps eating; a meal cut short keeps the rest on your tray (`SHIP.player.trayLeft`, not saved) and says so; the open needs strip closes on a deck tap, nothing more; a counter tap beside the staff, not on them, is the counter | with RV10, for 0.92.2 |

## Find-the-cause notes (for whoever picks these up)
- 0.92.0 trial (IM1 round 10): the bar failures and the Clock-in pins were arrows-c's check (AC3 fixed them); the 3
  updateWorldMatrix page errors were the floor tap above, exposed by arrows-c's mis-aimed FB1 taps.
- intro_check part 13 booth line: check timing (all four booths held by crew at 18:26); FX5 fixed the check line.
- LEAD31-12 (open): FE2 item 35 (a meal restarted with no touch for 270 s, the Long table's own words) and item 38 (no
  Eating line, Food flat for about 9 min at a café table). Neither reproduced with real taps; mess-taps keeps the tray.
- LEAD31-10 (open): taps on empty mess chairs at dinner open crew cards (crewAtScreen before the pick), as the counter did.
- LEAD31-14 (in progress when I stopped): see "Open" below.

## Open
- LEAD31-14, the Day 9 "Food" arrow (arrows_check's follower stuck from 16:50 with the Line on). Found so far on
  54efee21: the hunger arrow (needGoal, section 15) picks the nearest servery-queue or grab-shelf place, which from
  Decks 3 and 5 is the grab shelf 3-grab-1. A grab gives +25 over 3 minutes; the arrow clears only at Food 40 (WARN_REARM),
  so from near 0 it takes two grabs, and after the first the arrow still points at the shelf you just ate from. On paper
  only Brennan holds 3-grab-1 (5 min at 16:30 on Day 9); real taps from 16:50 to 20:00 all gave a hot plate. Asked FX6
  (session_01VVgFPg2QfrvjGSfxf7QsQw) for the follower's actions and toasts on Day 9 16:40-20:00 to see what it got.

## How to test (what I ran)
- Setup in a fresh container: `pip install playwright numpy pillow`; three r128 and acorn in /tmp/cadet-work (testing
  guide section 2); `CADET_CHROME=/opt/pw-browsers/chromium` for every check outside check_fast.
- Real-tap probes: project a world point (`new THREE.Vector3(x, y, z).project(camera)`) and `page.mouse.click`; turn the
  camera with `page.click('#rot')` then about 80 steps. Turn the arrows' pop-up queue off once after load:
  `if (GUIDE_ON) { GUIDE.tq.length = 0; guideToast = () => false; }`.
- To find who started or ended an activity: a copy of the game with a stack push at the top of actStart and actEnd.

## Gotchas
- Don't name a probe variable `HOOK`: cadet_test's own HOOK (window.__sc) is exec'd into your globals and the game then
  "fails to start".
- interactions_check's blocks are top-level `with` statements; to run one alone, split with Python's ast (top-level
  statements), not by lines: its JS strings hold lines at column 0.
- tiles_check's "Quick game" click times out under load: run it alone or two at a time.
- The container restarts now and then: background check runs are lost; rerun them (outputs written so far survive).
</content>
</invoke>
