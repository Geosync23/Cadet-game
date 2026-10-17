# Re-review: claude/sim-engineer 236810f..e4d6ace (0.26.35-0.26.37)

Reviewer 1, 2026-10-17. **Verdict: PASS.** 0.26.37 fixes the open must-fix, and it also fixes the must-fix I found in 0.26.36 (below). Nothing left that must be fixed for 0.60.3. 0.60.3 should take **0.26.36 and 0.26.37 together**: 0.26.36 on its own fails (seated diners and sleeping bunkmates get up, and squeezing past the cook breaks).

Follows sim-engineer-6e87e6b.md and sim-engineer-236810f.md.

## Must-fix status
- **CLOSED: Calder's arrival seat 3-mess-9 shared with Torres (6e87e6b, finding 1).** In 0.26.37, introLay's `free()` also refuses an `occ.res` hold for anyone else (`'intro:<other>'`) or an event. When no alternative is free, the beat gets no place; it no longer falls back to the named place.
  - Before the fix (merge with ship-events, sim at e1bb1e6), day_check 0 still failed: `['3-mess-9 torres-zeke/calder@1105']`.
  - After the fix, day_check part 5 reports "places booked twice: none" on days **0, 7, 35 and 1** without ship-events, and on days **0, 7 and 35** with ship-events. Every one of those runs ends DAY CHECK OK.
  - **Calder** (probe on both merges, identical results): booked at 3-mess-9 from 18:25 to 20:00 on day 0, and `planWhere` puts him there at 18:30 and 19:00. The `occ.res` hold `intro:calder` covers 18:25-20:00. The only other booking of 3-mess-9 that evening is vasquez-uma, 17:29-18:03, which ends before Calder's.
  - **Torres:** his ordinary dinner seat is 3-mess-11 (18:00-18:53). His intro beats stand in at the servery: 3-queue-2 at 18:20, 3-queue-1 at 18:30, and he's on to 3-tend-1 by 19:00. On screen, section 21's escort seats him at 3-mess-12 ("his seat 3-mess-12" in intro_check part 8). Torres is never at 3-mess-9.
  - **No alternative free:** I booked every alternative for each beat that has them (Torres's works, lift, toMess, servery and table beats; the day-1 briefing for Calder and Torres; Brennan's day-1 dinner) and laid them with `introLay`. Each comes out as `[deck, null, 'intro']`: the right deck, no place, nobody double-booked. In play, a crew member with no place stands where they are (`retarget(null)` keeps them on an open tile). Nobody gets stuck: worst stuck is 0.0 ship minutes on every deck on every day run.
- **CLOSED: 0.26.36 made seated and sleeping crew get up (found in this review, fixed by 0.26.37 before I reported it).** 0.26.36's `sharedTile` matches far more than the cook's station: 27 shared tiles on Deck 3 (mess seat pairs, lounge seats, benches with lantern spots), 22 on Deck 4 (every bunk aisle tile, laundry), 23 on Deck 2 (cabin wash units). Probe on the merge with sim at e1bb1e6:
  - You sit at 3-mess-27: Sato, sitting at 3-mess-12 (same walk-to tile [29,2]), stands up mid-dinner and stands at [28,0] until his plan moves on.
  - You lie in your bunk 4-B1-4 at 23:30: both sleeping bunkmates (santos-zofia at 4-B1-3, dlamini-lukas at 4-B1-5) get up and stand in the aisle for as long as you lie there.
  - In 0.26.37 only crew standing at their place (`spot.onTile`) or on a tile cleared by `crewMakeWay` step aside. The same probe on the new merge: Sato stays seated, and both bunkmates stay lying down (8 samples, 23:34-23:41).

## 0.26.36/0.26.37 crewMakeWay (the cook steps aside), checked
- **The player can use the shared tile:** probe on the merge with ship-events, sim at e1bb1e6. Brennan is cooking at 3-galley-2 at 07:26 on day 1. You head for 3-range-1-panel: Brennan goes to [38,4], you reach [39,4] and use the panel ("do" for about 7 ship minutes). After `actEnd`, Brennan goes back and settles at 3-galley-2 ('work' pose) within 2 ship minutes. The galley's cooking runs on paper, so stepping aside doesn't change the food. player_check on ME (squeeze past the chef, the range panel) was still queued behind the shared browser lock when I wrote this; its output will be in /tmp/cadet-work/rv-sim37tools/player-me.out. The sim engineer reports player_check OK on the branch and on sim + galley 0.29.34.
- **Not pushed into walls, through blocked tiles or into other seats:** `asideTile` takes only `free()` tiles in the same room, and the path is `crewPath`. Brennan's aside tile [38,4] is free and not blocked.
- **Deterministic:** plans aren't touched. `crewWayOn` reads only the player's goal and place and `shipNow()`, and `asideTile` scans in a fixed order. Entering a deck (`deckCrewFill`, also after a sleep) clears `CREW_WAY`, so a jump never carries a make-way. On both merges, "Plans the same twice: True" and "Deck 4 the same twice: True" on every day run.
- **Crew who make way still finish their task:** the plan is unchanged and the crew member goes back when the way clears. A crewMakeWay hold lapses after `mins` (10) ship minutes even if the release function is never called.

## Findings (none must be fixed)
1. **Low (phones): `crewWayOn(now)` allocates in every crew member's update, every frame.** It builds a 2-element array and a filtered copy each call, even when nothing is being cleared. While you're heading for, or using, a place on a shared tile, it also builds a new Map for each crew member every frame (about 70 per frame at dinner). Fix: compute the way once per frame in `updateDeckCrew` and pass it in, and return early when `CREW_WAY.size === 0 && !player.path.length && !PLAYER_PLACE`.
2. **Low: `asideTile` can pick a tile another person's station stands on, or another shared tile.** The cook went to [38,4], which is the walk-to tile of 3-galley-4 and of 3-oven-2-panel. If a second cook were settled at 3-galley-4, the two would overlap on one tile. Fix: skip tiles in `occupiedBy(null)` and tiles any place's spot stands on (the `SHARED_T` key set has the counts).
3. **Low: a crew member walking off a seat whose walk-to tile is shared with the place you're using takes a short detour.** `!this.settled && way.has(here)` sends them '@aside' for a moment. Seen: Sato leaving 3-mess-12 at 18:56 while you sat at 3-mess-27. He went on to the lift a few seconds later. Cosmetic.
4. **Low (arrival, not this branch): the beats with alternatives choose among every place in the room nearest the tile.** That includes queue spots: Torres's "table" stand-in is 3-queue-2. The player's named seat 3-mess-10 is also booked by volkov-maeve from 18:00 to 18:51 on day 0. Your seat isn't held in `occ.res`. Section 15's "someone got there first" picks a nearby free seat, so it's playable, but it's worth a look by the arrival owner.
5. **0.26.35 (the Tern start [5,7]) is not in 0.60.3** (the lead's recipe has it in 0.60.4). Neither merge includes decks-p3, so the Tern isn't walkable there: intro_check part 8 shows you and Torres starting at Deck 5 [5,11] (nearestOpen moved you), and the beats still pass. Ship 0.26.35 only together with decks 0.38.19 or later (decks-p3; `5-tern-aisle-1` is only there).

## Merges and tests
- **M** = origin/claude/arrival 9b37dd9 + sim-engineer e4d6ace + deck-plans-1-2-6 55e98e7 + social 9e0d46e + social-stories 74b25e1 + player-needs 9c18045 + galley-food 7464b97. **ME** = M + ship-events 2ffff6f.
  - Plain merges, no `-X`, no ship-systems.
  - **Conflicts:** the build lines (kept arrival's); DEV_NOTES and design-doc (kept both sides). One build-line conflict also held arrival's simNote/flag block next to it, against deck-plans' bare build line; I kept the block.
  - **Test files, newer kept:** player_check.py was social's at first, then player-needs' (newer); cadet_test.py is player-needs' (newer).
- **name_check:** `--branches 236810f e4d6ace` NAMES OK (6 new names). M and ME: NAMES OK, node --check parses.
- **day_check** (part 5 "places booked twice: none" in every run below):
  - **M, days 0, 7, 35 and 1:** all OK.
    - Servery: day 0 77/77 served; day 1 128/128 served, 125 trays out and 125 back; nobody gave up.
    - Worst stuck: 0.0 ship minutes.
    - Draw calls, Deck 3 peak: 276 / 268 / 263 / 278 (budget 450).
  - **ME, days 0, 7 and 35:** all OK. The numbers are identical to M; ship-events' 2ffff6f mostly concerns New game resets. Day 1 on ME is still queued (it will be in dc-me-1.out); day 1 on M passes.
- **intro_check (arrival's) parts 8, 9 and 11:**
  - **M: OK.**
    - Part 8: the whole evening (ramp to night) with Torres leading, draw-call peaks 171/208/281.
    - Part 9: a first launch is saved at the ramp and loads at the ramp.
    - Part 11: reloading mid-walk at 'wing' keeps Torres leading, and you still reach your bunk.
  - **ME:** parts 8, 9 and 11 give the same results as M (the same beats, positions and draw-call peaks). Part 10 onward was still running when I wrote this (intro-me.out).
- Workspace: CADET_WORK=/tmp/cadet-work/rv-sim37work. Probes are in /tmp/cadet-work/rv-sim37tools: `shared.js` (the shared tiles), `way1.js` (diner and bunk), `way2.js` (the cook), `arr.js` (arrival seats, no free alternative).
