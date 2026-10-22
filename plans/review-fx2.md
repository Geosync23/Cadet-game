# Review: the Pillar 5 fixes FX1-FX3 (AR2; FX2 from the start, FX1 and FX3 from PR9 at lead 28's call)

Reviewer AR2 (session_015pnwa5oK7TDF5gZXNFLLvx), for lead 27, taking over FX2 from PR9. Base: claude/integration 2b4a05db (0.64.15). Builder FX2: session_01JRCSTi6r1qQ51mTgwgJ7es.

How each part is judged (lead 27's brief): its new check part FAILs on 2b4a05db and passes on the tip; honest play in the browser (AR2's bot: it follows only the arrow, taps what the arrow names, uses the board and reads meetings through); cadet_test 2b4a05db -> tip run alone, identical except what's intended; AR1's `arrows_check.py week` (claude/arrows-plan) to see FX2's lines turn green and nothing turn red; clashes with FX1 (claude/p5-fix1) and FX3 (claude/p5-fix3) in sections 15, 15b and 24.

## A. The fire drill (e10d81a4): FIXES NEEDED (one item)

| Test | Result |
| --- | --- |
| mech_check m3d, new "drill by taps" part, on 2b4a05db | FAIL (4 lines: Calendar place, each tap starts nothing, no stop done, no extinguisher), as it should |
| the same on e10d81a4 | MECH CHECK OK |
| cadet_test 2b4a05db -> e10d81a4 | ALL IDENTICAL |
| Honest play, Day 3 (Rounds trained Day 2) | 14:50 toast and "Fire drill, 15:00" on the extinguisher; tap: "Fire drill: about 1 minutes"; arrow "Stand by the hatch"; 10 minutes; "The extinguisher back on its bracket"; "Fire drill: done." at 15:05; 15:15 "Trained: the drill", "All clear", "Two minutes ten. Better."; the arrow gone after the last stop. The bot took a board job straight after. |
| arrows_check week on e10d81a4 | Green now (FAIL on base): Day 3 "m3d" not learned; "stuck from Day 3 14:50 at Fire drill, 15:00"; "Fire drill stayed up over 3 hours"; and "Day 4/5: never clocked in" (they followed from the drill block). Red now, new: "stuck Day 3 15:15 at Repair the galley plant", "stuck Day 4 08:04 and 11:39 at Look over the stage lights (Deck 7)" and its "stayed up" line. Both are old problems the run now reaches because it no longer sticks at the drill: the galley plant one is on base already (09:18); the stage lights' arrow and taps are the same on base and tip (probe: jobHere at 7-aud-lights-svc works on both), and FX2 didn't touch the machine arrow or taps. Not FX2's. |
| Trial merge FX2 + FX3 b063f86 + FX1 1433e5f | Conflict only in plans/build-table.md. Played Day 3 on the merge: FX3's Calder briefing shows at 14:50 (before the drill, as it should), then FX2's arrows take you through; all done at 15:05. No clash in setGoal/clearGoal: drillGoal only touches a goal tagged with the drill's id. |

**Fix needed (A1).** The drill job is posted and claimed for you at the 14:00 hour (`post(h)` with h = 14; `found` = 14:50), and `ixSides()` offers it at once. So from 14:00 to 14:50, before Calder's call, a tap on the extinguisher (on the Works bay wall by the board, the sort of thing players tap to read) starts the drill silently. Reproduced at 14:13: "Fire drill: about 1 minutes", the extinguisher in your hand, `j.reached` = -45 (a "fast" muster), and at 14:50 the toast and arrow point at a stop already done. Suggested: `ixSides()` only offers a side job once it's announced (`j.found <= shipNow()`, or `j.told` for the drill); before that the tap shows the extinguisher's description as before. One line in the m3d part (a tap at 14:20 starts nothing) holds it.

**Notes (not blocking):** the step toasts are titled "Your job" and say "about 1 minutes" (old wording in 15b's chore path); Calder's word "Two minutes ten" is a fixed line, not the real time (old).

## FX2 tip cc2bb2be (A1 a76ec6c0, B 03f9eb9f + a3b93ced + cc2bb2be, C 1ae2d27c): PASS

In it: A1, no side-job taps before the job is announced (`ixSides`: `!(j.found > shipNow())`). B: scan first on every faulty job once you have the scanner (`scanFirst`: the arrow says "Look over the <machine>", the look-over fits nothing and opens the scanner; the part is named after the reading); the use counts with no Fetch pressed (`scanFitted` takes the named part); jobEnd now asks 24k's `caseFitted` (a repair before the head-scratcher is called leaves the machine faulty); the teacher's watch job is off your board for every lesson (`worksWatching` in `jobsBoard` and `boardForYou`); m7 trains only once scanned (`WORK_MECH.m7.counts`); the clue toast has a title. C: one time and place in the Tuning and Hauling asks, "Tune the" on a tune job's arrow, the inspection's Calendar time 06:30.

| Test | Result |
| --- | --- |
| mech_check m3d m7 m4 m5 on 2b4a05db | FAIL: the drill by taps (6 lines), m7's clue toast, scan first, the use count, "a repair before the call leaves it faulty", "a training job finished without a scan doesn't train you" (and the fix2 part), as they should |
| mech_check (all parts) on cc2bb2be | MECH CHECK OK |
| puzzle_check, career_check on cc2bb2be | OK, both (jobEnd's caseFitted touches every head-scratcher) |
| cadet_test 2b4a05db -> cc2bb2be | ALL IDENTICAL |
| A1 by hand | a tap on the extinguisher at 14:13: nothing starts (e10d81a4 started the drill) |
| Honest play Days 2-8 (follower, drops a job to take a training) | Hauling and Tuning: the teacher's job is no longer on your board while you watch (board at 12:50 lists only your run; Day 4 only "Tune: Oven 2"); Day 5: after the watch "Repair: Washer 2 (leaks)", the arrow "Look over the washer", "You open the panel... with the scanner", the clue toasts "Fault notes / + clue: Eklund", the case called, "Trained: the scanner" at 10:37; afterwards "Look over the seat hinges", the scanner reads, then Fetch; Day 8: Making it safe opens (the use counted) and Calder's call comes at 10:30 (its wrong-deck arrow is FX3's fix, passed) |
| arrows_check week on cc2bb2be | as on e10d81a4; the m7/p3/scanner/m6 lines can't turn green on FX2 alone, as the follower's chain still stops at Day 2's m1 (FX1). Nothing new red |

Not in this push (from lead 27's list for C): the galley plant's calibrate (the stuck "Repair the galley plant" arrow; arrows_check names "nobody yet") and a dropped job's part left in hand (backlog AR2-1). Asked FX2 whether they're coming or someone else's.

Watch for (not FX2's): during a lesson's watch step there's still no arrow, so a follower only gets through it by being near the teacher by chance (Day 4's tuning watch took 08:46-10:22). That's the arrows plan's T2 (follow the teacher).

## FX3's delta e6bcf827 (on b063f86, which PR9 passed with fixes): PASS

In it: hauling's lesson on any day from Day 3 (the week's `manifestFor` crates kept back for it) and asked again at its own time (`againAsk`), not at 06:00; each manifest stop's own words on the arrow (a kind's `goal(j, k)`, read by 15b's `ixJobStep`; `haulName` knows "linen"); the promotion talk where Calder finds you (`where: { any: true }`); 24f clears only its own arrow (`incGoalSet`/`incGoalClear`, PR9's request); Tomas's inspection ask in person in Bunk 1 18:00-21:30 the evening before, else Mail at 21:30.

| Test | Result |
| --- | --- |
| mech_check fx3 on 2b4a05db | FAIL (promo talk; m4 off a delivery day, its run, per-stop words, the retry time; m6's Mail, warning, follow, crew and retry), as it should |
| mech_check fx3, and m4 m6 m3i, on e6bcf827 | MECH CHECK OK, both |
| cadet_test 2b4a05db -> e6bcf827 | first run: only `a_start` 14812 px (the known first-frame bubble flake, backlog #16); rerun ALL IDENTICAL (renderer noise only) |
| Honest play, Thursday case (Rounds trained Day 3, hauling not; manifest empty) | base: Yara's talk at 11:40, then `again`, nothing (the old stall). tip: talk at 11:40, watch, the run "Manifest run: 1 crate" held for you, trained at 11:57 |
| Honest play, Days 2-5 | per-stop words seen: "Take a hover cart from the Cart bay", "Load the medical supplies (1 of 2)", "Load the crew store stock (2 of 2)", "Medical supplies to the infirmary, Deck 3", "Crew store stock to the crew store, Deck 3", "Cart back to its dock" |
| arrows_check week on e6bcf827 | the same 17 FAILs as PR9's b063f86 run (main lift lines stay green; Day 2 "Repair the light relays" stale arrow still red, FX1's); nothing new red |

Seen, not FX3's: in both runs the follower took Yara's own "load only" watch run from the board ("[train] [held]") and was trained after one load, without delivering anything. That is the teacher's-job item in FX2's B (sent to FX2: cover hauling, not only the scanner). Yara's Mail still says "Meet me at the hold" (FX2's C).

## FX3's delta 360801c0 (fixes 8 and 9, from FX2's list by lead 28): PASS

In it: (8) calibrating the galley plant: a tap whose line passes over your job's pin starts your machine's work even if the chiller in front caught the tap (15's jobTap), and a machine chore's arrow shows its own title ("Calibrate the galley plant"); (9) a part in your hands that nothing you hold needs gets "Put the relay back: main storage" (15b's `ixLoose`), a shelf tap puts it back.

| Test | Result |
| --- | --- |
| interactions_check on 2b4a05db | FAIL: "Repair the galley plant", "Cold store chiller: in good order.", no put-back arrow (twice), as it should |
| interactions_check, player_check on 360801c0 | OK, both |
| cadet_test 2b4a05db -> 360801c0 | ALL IDENTICAL |
| By hand | a relay in hand, no job: after "Clock in", the arrow is "Put the relay back: main storage" at the Lights shelf; a tap on the shelf: "You put back a relay.", then "Take a job at the job board" |
| arrows_check week on 360801c0 | green now: every "stuck at Repair the galley plant", "Look over the stage lights" and "Repair the light relays" line. New red: Days 3/4/5/8 "never clocked in" and the arrow "Take your first round at the job board" up from Day 2 11:08, and "Fire drill, 15:00" up for days. With the galley plant fixed the follower now reaches Torres's talk, lapses the round (m1 `again`) and meets FX1's known "Take your first round" arrow over Clock in, and FX2's not-yet-merged drill arrow |
| arrows_check week on a merge FX2 cc2bb2be + FX3 360801c0 (AC1's resolution of the one-line conflict) | the drill lines go; left: the same m1 chain (FX1) and one line "Turn it in at the job board stayed up from Day 4 05:50" on that path only. My own play of the merge (Days 2-4) doesn't show it: there the round is learned on Day 2, Yara's lesson lapses on Day 3 and FX3's re-ask comes on Day 4 with FX2's words ("Meet me in Main storage on Deck 5, 11:40"). To look at again once FX1 is in |

Merge: FX2 and FX3 conflict in one line of 15b's ixJobStep (the machine arrow's label: FX2's scan-first and "Tune the", FX3's chore title) and in mech_check.py; AC1's claude/arrows-c 1f2ce27d resolves the line as both (checked).

## FX2's eating fix 191d1853 (on a merge of integration b9f053ba): PASS

With a tray, only a `mess-seat` ate it; now any sit place does (`SIT_TYPES` with pose `sit`: lounge seats, benches, the common room, the garden, the music room's seats, event seats such as Sunday's long table, the observatory). Only when you hold a tray.

| Test | Result |
| --- | --- |
| player_check on b9f053ba | FAIL "with a tray, a tap on any seat eats it" (long table, lounge, mess seat all 'sit'), as it should |
| player_check on 191d1853 | PLAYER CHECK OK |
| cadet_test b9f053ba -> 191d1853 | ALL IDENTICAL |
| By hand (Deck 3, 18:30) | no tray: lounge seat, mess seat, bench all "Sitting" on both builds (unchanged); with a tray: base eats only at the mess seat, the tip eats at all three |
| Other sit-downs and the crew | the change is inside the player's `actStart` tray branch only: meetings, traditions and the lounge without a tray are unchanged (above), and the crew's seating (sections 10 and 14) isn't touched |

Note for the user, not blocking: "any seat" includes the music room's seats (the piano stool) and meeting seats (`event`), so a tray carried into a meeting room is eaten there.

## FX3's delta 02e212f1 (fix 10, the lift-panel arrow; the user's go): PASS

A goal on another deck now points at the nearest Lift panel you can see (`ixLiftPanel`: section 11's `lift` items, a hidden one only if none shows), not the middle of the landing, labelled "Tap the lift: Deck N · <goal>" (a trailing ", Deck N" said once).

| Test | Result |
| --- | --- |
| interactions_check on 2b4a05db | FAIL: "another deck: the lift panel", "parts in hand: to the machine", the Deck 5 inside label and "the arrow points at a lift panel you can see, not the landing (166.8 px)" (and fixes 8-9's lines), as they should |
| interactions_check on 02e212f1 | INTERACTIONS CHECK OK |
| intro_check --evening on 2b4a05db / 02e212f1 | FAIL "at the Deck 5 lift with Torres, the arrow should point at the lift panel" (label was "Take the lift to Deck 4: zeke Torres", lower-case z) / OK |
| cadet_test 2b4a05db -> 02e212f1 | e_night to i_tap3 differ (about 12,000 px each), all else identical. Looked at e_night: the only change is the off-screen arrow's label ("Take the lift to Deck 3: food, Deck 3" -> "Tap the lift: Deck 3 · Food") and its angle. Intended |
| By eye, phone 390 x 844 | Deck 5, goal on Deck 4: the pin sits on the lift's keypad beside the doors, "Tap the lift: Deck 4 · Your bunk" (base: the landing's middle). Deck 4 in Bunk 1, goal on Deck 3: off screen, an edge arrow toward the lift, "Tap the lift: Deck 3 · Food" |

Shots: scratch only (lift_base_d5.png, lift_fx3d_d5.png).

## FX1 a34f4666 (1433e5f + the lifecycle commit 00a3a1dd; re-check from PR9): PASS, with one merge blocker for the lead

In it: tracking stays on (new game, Tracked items, every device "go" through `goTo`, which clears on arrival); a tracked job that's gone resets tracking (`trackFresh`); the training meeting's arrow from 15 minutes before (`trainArrow`, "Wait here: ..." in its room, back after a borrowed arrow), and while you hold a job a word 10 minutes before instead ("Rounds with Zeke, 10:45, Works bay. In ten minutes: Tracked shows the way."); the round's arrow only after clock-in, only while the board offers it, never while you hold another job; On shift in Tracked is your job's arrow; career arrows carry `trk` ends (Meet Ines, the Chief's office, the cabin, the test job, the commission, the 14:50 drill); "Shift over: clock out" from 17:00 over a job; an empty-board word; the shower arrow's own-deck rule; lessons not before 09:15; Tracked names the teacher; a tap on the light relays by name.

| Test | Result |
| --- | --- |
| career_check --fx on 2b4a05db | FAIL, 15 lines (bug 1, bug 2, the borrowed arrow, new game, go, On shift, clock out, empty board, shower, 09:15, Tracked's names, the test job, the round's arrow, the light relays), as it should |
| career_check --fx on a34f4666 | CAREER CHECK OK |
| cadet_test 2b4a05db -> a34f4666 | first run: only `a_start` (the known first-frame flake); rerun ALL IDENTICAL |
| arrows_check week on a34f4666 alone | PR9's regression is gone: no "never clocked in" on any day, no "Take your first round" over Clock in, no stale drill or light-relays arrow. Left: the lesson chain (m1 still `ask` for this follower, then everything after) and FX2's/FX3's own lines (main lift, galley plant, stage lights), fixed on their branches |
| Honest play, merge FX3 02e212f1 + FX2 cc2bb2be + FX1 (my bot, Days 2-8) | Rounds learned on Day 2 (holding a job at 10:35: the word "In ten minutes: Tracked shows the way", then Tracked); "Wait here: hauling and stores with Yara, 12:00" in Main storage; "Shift over: clock out" at 17:00; "Nothing on the board for you just now" when dry; the drill learned. **Then Hauling's watch step lapses every day (Days 3, 4, 5) and nothing after it opens.** See below |
| arrows_check week on the merge | no clock-in line red on any day; drill learned. Red: the lesson chain (m1 `again` for this follower), "Take your first round" stuck at the board Days 3 and 8, and "Clean a vent: laundry" stuck Days 2 and 4 |
| arrows_check shift on the merge | "not clocked out" (the check reads careerClockedIn, which stays true after clocking out: FX1's note, for AR1) and "stuck at Take clean linen to the laundry, Deck 4" |

**Merge blocker (not one fixer's bug):** with FX2's fix the teacher's job is off your board during the watch step, and nothing points at the watch step: after Yara's talk the job arrow says "Take a job at the job board", the follower goes off on other jobs and is never within 3 tiles of her run for 10 minutes, so the lesson lapses at 17:00 every day. Before FX2 a player could take the teacher's job (a skip); now there's no way through but luck. Same for Tuning and the scanner. Suggested: while `c.st === 'watch'`, an arrow to the training job's spot or the teacher ("Watch Yara: Main storage"), over board and job arrows, until your turn. Sent to lead 29 and FX1.

**Merge resolutions (FX1 with FX2/FX3), four code conflicts:** 15's jobTap (FX1's `own` + FX3's room fallback and ray rescue: both); 15b's ixJobStep (FX1's "Shift over" first, then FX3's put-back); the 14:50 drill arrow: **FX2's must win**: FX1's `trk: 'career:drill'` (no trkFrom) makes trkDoneCheck clear it as soon as you reach the Works bay, before FX2's stop-by-stop drill arrows (drillGoal only moves an arrow tagged with the drill), and FX2 already clears it at 15:15; "Meet Ines": FX3's incGoalSet with FX1's trk fields (fine).

**Found, old (on 2b4a05db too), not FX1's:** the laundry's chore pin (`4-laundry-1`, "Clean a vent: laundry" and "Take clean linen to the laundry") sits on Washer 1: a tap on the washer starts your own laundry load ("You start a load. It fills and begins to churn.") instead of the chore's stop; only a floor tap at the pin works. The same shape as the galley plant/chiller case FX3 fixed. That's both stuck lines above.

## AC1's watch-step arrow 90992e66 (claude/arrows-c 86a980c5, on FX1 + FX2 + FX3 360801c0): PASS with the queue off; queue on has the next gap

While a lesson is at 'watch', a direct arrow on the training job's spot ("Watch Yara: Cargo hold"), over the board and job arrows, another section's arrow left alone, down at your turn; nothing with the queue on (E's T2 instead).

| Test | Result |
| --- | --- |
| Honest play Days 2-5, queue off (my bot) | every lesson learned by following the arrow: Rounds (Day 2), Hauling ("Watch Yara: Cargo hold" 12:05, your turn 12:15, trained 12:36), the drill, Tuning ("Watch Calder: Galley" 09:32, trained 09:50), the scanner ("Watch Emeka: Laundry" 09:51, your turn on Washer 2, trained 10:43). Before it (my FX1+FX2+FX3 merge): Hauling lapsed every day |
| Honest play Days 2-5, queue on (GUIDE_ON true) | the watch steps complete (T2), but each lesson's turn then lapses at 17:00 (Hauling `do` on Days 3, 4 and 5): the 'do' gap FX2 is fixing. Also "Trained: rounds" toasted twice (11:09 and 11:12) |
| arrows_check week on 86a980c5 | as on my 3-way merge: AR1's follower (no Tracked) lets Rounds lapse on Day 2 (holding a job, FX1 gives a word, not an arrow), then "stuck at Take your first round" Days 3 and 8, and the laundry pin (FX3's next). By hand in that state (m1 `again`, Day 3, clocked in) the board offers "Your first round, Deck 4" and Take it works: the stuck line looks like the follower's, for AR1 |

## FX3 8aae0634 (fixes 11-13 on 02e212f1) and plans/fx3-lift-alone.patch on b9f053ba (for BM14): PASS, both

In it: (11) low energy's "Your bunk" arrow only at bedtime or unwell, cleared once you lie down; (12) a check for the climbing holds' pin (fixed by fix 8); (13) your turn at the burst pipe parks a job you hold (`claimedBy: 'you-parked'`, its progress kept) and gives it back after; 24f's labels say Calder.

| Test | Result |
| --- | --- |
| player_check, interactions_check, mech_check fx3 on 2b4a05db | FAIL (2, 25 and 18 lines, among them the low-energy bunk arrow, the holds' pin starting a climb, the held job waiting at the pipe, "Meet Ines" for Calder), as they should |
| the same on 8aae0634 | OK, all three |
| cadet_test 2b4a05db -> 8aae0634 | only e_night to i_tap3, with exactly 02e212f1's counts (the lift-panel arrow, checked by eye before) |
| Parking by hand | a repair with a part fitted, parked: `you-parked`; two ship hours on, the crew's finish rule (claimed, not 'you', `done` passed) leaves it alone (`done` unset); through JSON and jobsTidy it stays; given back as yours with its fitted part |
| The lift patch alone on b9f053ba (f93bde5a when applied) | interactions_check FAILs on b9f053ba (4 lift lines) and is OK patched; intro_check --evening OK patched; cadet_test b9f053ba -> patched: the same shots and counts as on 2b4a05db (the arrow only) |

Cosmetic, not blocking: the job board's crew list shows a parked job as taken (its "taken" rows are any claimedBy but 'you').
