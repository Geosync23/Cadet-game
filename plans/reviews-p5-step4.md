# Reviews: Pillar 5 Step 3 last piece and Step 4 (reviewers R4, then R5)

R4 succeeds R3 (whose verdicts are in `plans/reviews-p5-step2.md`). R5 (session_01XJyHzg4QvX2nsdtf9zT1TH) takes over from R4 at ~06:00. Newest first.

## Playtest update 2 (brief: plans/brief-playtest2.md on claude/lead-pillar1; build master BM7 session_01QbuzvT3TwzMwSWRmakzX8Z)

### X claude/crew-pt1 056f8d8 (0.71.3, crew-sim playtest 2 items 2, 8, 13, 14, 16, 21, 22): PASS WITH FIXES (X has handed over: the next crew-sim seat answers)
X's commits 0e112d69..056f8d8 on 7a6e137 (no merges). Read with a helper agent against plans/brief-playtest2.md; fix 1 confirmed by hand.
- Done: 21/22, crew wake about 30 minutes earlier and are spread out (schedU keys 10 and k+4; bar staff +45; breakfast 06:50-08:30); 2, Calder sits at the Day 1 dinner (introBeats starts the Chief's beat at the table step); 16, the rower's handle moves (noMerge, about +1 draw call per rower); 13, tapping the beam (or the floor near it) paints your name; 14, up to 8 crew say `beam.congrats` from W2's banks (the words are the writer's; BEAM_CHEERS is only timing). Nothing saved, no R(), `node --check` passes, no names shared with U/E1/E2/E3; a trial merge conflicts only on the build lines.
- **Fix 1 (item 8 does nothing): `withHold` (~10339) returns at once when the stop already has `w.hold`**, and every crew load/unload stop already has one (restock 'cart'/'cartfull', haul's load stop 'cartfull'), so the new 'carry' branch is never reached. It also only covers jobs, not crew at the Wednesday delivery (`5-delivery-1`, anim 'lift', which holds dumbbells). Check in the game what the user saw and put the crate on those stops.
- **Fix 2 (items 15/20 are missing): the booth and shower queues aren't built** (X's handover: "not started"). U needs a function to read for "You're 2nd in line" (W2's queue.* keys exist). It needs an owner (lead 17) and an agreed shape with U.
- Notes: lines written for the old dinner are now stale (Torres's "Oh. Look who's coming over" in introDinner, the tip "the Chief's coming over"): for W2. Item 2 reverses the user's 0.42.64 ask (the Chief walks over after you sit); the brief asks for it, so it's fine, but worth saying in the report. The handle swings about every 2 s against a body loop of about 2.4 s, so they drift apart. Any floor tap within 2.5 tiles of the beam starts the painting while the tradition is on. W2's beam-all.lines isn't baked in this build yet, so non-Works crew say the fallback.
- Checks on 056f8d8: day_check (Day 2) OK. intro_check and cadet_test vs 7a6e137 were still running at R4's handover (X's handover expects a Deck 4 morning difference in cadet_test: the earlier wake times); R5, please read them in R4's scratchpad or re-run them.

### W2 claude/writer-p5 606e204 (0.48.112, queue.left for X2): PASS
Bakes 9565 lines; lines_check PASS. W2's tip.

### W2 claude/writer-p5 6a5d34a (0.48.104, the lines for items 1, 5, 9, 14, 15/20, 19): PASS
Lines skimmed. In a fresh archive content_gen bakes 9342 lines; lines_check PASS (0 errors, the 2 old "(Say nothing)" warnings). New placeholders `nth`, `start` are added to lines_check. `beam.congrats` is in both beam.lines (`@bank dept:works`) and the new beam-all.lines (`@bank all`): two different banks, so Works crew keep theirs and everyone else gets the new ones; not a clash. Torres's M1 meeting now explains rounds and sends you to the board (item 1). Builders, please note: `tip.round.look` says "Tap Look." (E1/U's button must be called Look), and `alarm.energy` shows a percentage, as item 5 asks.

## Step 4

### E6 claude/mech-rounds 2edb69c8 (0.45.14, R5's two fixes on E1's 0.45.11/0.45.12), R5: PASS
E6 took E1's seat. Diff 013f53ec..2edb69c8.
- logbookTick: only a worn flagged machine is serviced, never a faulty one, never a job held for you (heldForYou, section 17, defined earlier in the file).
- Turn-in: side kinds pay (WORK_XP ?? 1) + 1 if right first time, still capped. Only rewiring sets j.rightFirst among side kinds (the other setters are scanFitted and 24k's cases, both repairs), so a leak stays +1 and the joint chore (j.xp 0) 0; mech_check side pays [2, 0, 1] and m12 leaves a failing machine and a held job open.
- Still open on E6: 0.45.13's load-stop order (haulStops).
- Checks: on a merge with E3's places, queued.

### E5 claude/mech-incidents 60a418fe (0.51.13; contains 93fbdb5d 0.51.12), R5: PASS
E5 took E2's seat. Diff 67144486..60a418fe.
- The pin: `playerRigRebuild()` in 24l (lead 17: E2's, now E5's), the same steps as 24p's promoPip (old rig removed and its geometry freed, makeCharacter(spec) again, props reset, the grubby tint put back) plus the stand-in at a place (recBody). makeCharacter draws no R(), so no determinism change. ffPin can now show the pin; mech_check checks it merged into the chest and back after a reload.
- A leak +1 in all: leakDone no longer sets foundBy (side.leaks keeps found); mech_check checks the pay with E1's flat turn-in.
- Note: promoPip and playerRigRebuild are now two copies of the same rebuild; promoPip could call playerRigRebuild (24p's owner, later; no fix asked).
- Open elsewhere: rewiring's right-first +1 (E6's, see E1's verdict); E5's trial with E1 633eade found it too.
- Checks on 60a418fe: running.

### E1 claude/mech-rounds 013f53ec (0.45.13, hauling stage 2: haulFree, haulOrderAsk, haulTidy), R5: PASS WITH FIXES (one small; E1 has handed over: E6 session_018cZuXpb4XdFs47zXoPcF8B does it, with the two on 0.45.11)
Diff 633eade..013f53ec, read by hand against step4-stages (D3's answers).
- Good: m4 stage 1 now after 2 runs; from Day 10 (haulFree) a manifest run with crates for 2+ stops asks you the order once (j.orderAsked), before any delivery, one deviceChoose per stop, Cancel keeps the rest; "A tidy run" (haul.tidy) when the deck changes are the fewest possible, +1 through worksSideXp for an officer only; an officer at stage 2 keeps the run held to 16:00. Parts runs (j.src) and load-only runs are left alone. New names haulFree/haulDeck/haulTidy/haulOrderAsk nowhere else. No R(); j.order/j.orderAsked live on the job (saved with the jobs).
- **Fix (small): the order also reshuffles the load stops.** haulStops sorts `cs` by j.order and builds BOTH the load and the deliver stops from it; stepsDone holds stop indexes. If a load is done before (or while) the order is picked (the deviceChoose is async, and during it j.order is partial, so unplaced crates sort first), index 0 can name a different crate afterwards: the wrong crate shows as loaded and haulTake's j.got goes out of step. Sort only the deliver stops (keep the loads in manifest order), or ask before the first load.
- Note: haulTidy doesn't count the trip back to the dock (fine, the same for every order).
- Checks: on a merge with E3's places, queued.

### E1 claude/mech-rounds 633eade (0.45.12, manifestRun) and fb499eb8 (0.45.11, M11 tool upkeep + M12 logbook, flat side rep, key order), R5: PASS WITH FIXES (two)
fb499eb8 read with a helper agent against m11/m12 (diff from b82c8e23); 633eade read by hand. Line numbers in 633eade.
- Good, M11: the bench (scanner charging 5 min as a wait a tick finishes, pipe kit 2-min hold, logger 1), back to Charged; +1 a week through worksSideXp when all are charged; stages [0,2,4], the rack from stage 2 with Calder's upkeep.rack. M12: workdays 16:30-17:30 at the notice board by 5-works-terminal, three summaries from the real work log/found notes/open jobs, order by schedU(d, 0, 1012) (the only key), one entry a day +1 capped, j.logged = 10% quicker for you and the crew, the flag from stage 1, the last 30 kept.
- Good, 24 core: side-kind turn-ins are flat (WORK_XP ?? 1, capped), `j.xp === 0` pays nothing: a leak pays exactly +1 (lead 17) and E2's worn joint 0. worksInit/worksClean put `side` last after `cur` (BM7's key order), old saves give {}. One owner: 23 new names (TOOL_UPKEEP, RACK_MINS, bench*, rackTap, LOGBOOK, logbook*, logChoices, logLast, nightWorks) nowhere else; hooks (actEnd's onDone, jobMins/jobRun multipliers) typeof-guarded and in the hook register. No R(), nothing drawn. Every key read exists on writer-p5.
- Good, manifestRun (0.45.12): a 'haul' job with j.src 'stores', crates keyed p0.. (old crates fall back to c.id), loaded from each part's shelf (shelfOf) and taken with takePart, held for you only (reserved slot 30) until o.until, withdrawn quietly by a tick if not delivered; delivery sets j.delivered and simNote('manifestRun'); the Wednesday manifest ignores parts runs (haulOpen/!j.src).
- **Fix 1 (bug, M12): the night crew finish jobs held for you, and more than the page allows.** logbookTick 40454-40455: `st !== 'healthy'` and `find(... && !x.claimedBy)` finishes reserved and case/ticket jobs held for you (heldForYou), breaking a running case or ticket, and services faulty machines too. The page: "a worn one is serviced early". Use `st === 'worn'` and skip heldForYou(x) jobs.
- **Fix 2 (cross-seat, rep): rewiring's right-first-time +1 is now paid by nobody.** The m15 page: "+1 (+1 more right first time)". Lead 17: right-first-time stays with E1's turn-in; E2's 0.51.11 dropped its own worksSideXp(1) accordingly, but the flat side formula (39740) ignores j.rightFirst. Count `right` for side kinds too (`(WORK_XP[kind] ?? 1) + (right ? 1 : 0)`, still through the cap), with a mech_check line (a side job with rightFirst pays 2, one with j.xp 0 pays 0, a leak with foundBy pays 1).
- Notes: playerRigRebuild is E5's now (lead 17), not E1's. Record line: W2's works.ms.stars is "Star logger" (no {n}); E1's fallback "Star logger, Day {n}." and the grade names (Senior/Master vs W2's Trusted / The ship's) differ: settle with W2. benchStart counts the use/training before the hold finishes (walking away still counts) and the scanner charge starts without walking you to the bench. logbookData doesn't check an entry's jobs/flag (junk throws at last.jobs.length, caught). Nothing calls logLast (page: progress talks call logLast(3)); log.talk is said instead. On a quiet day all three log choices read the same. The tester (m15) wears but has no bench upkeep and isn't in "all charged". The flag question is a second deviceChoose after 600 ms (lost if refused). manifestRun: takePart's result is ignored (an empty shelf still "loads" the part); two runs for the same asker in the same minute share an id. mech_check calls onDone/benchStart/logbookWrite directly (taps and time windows untested) and its save test is worksClean on a JSON copy, not a real save.
- Checks: on a merge of 633eade + E3's places 9d179e9 (and on E1+E2 0.51.11+places), running.

### E2 claude/mech-incidents 67144486 (0.51.11, E2's final: R5's fixes on 0.51.7-0.51.9), R5: PASS WITH FIXES (one, for E5)
Diff 3014b864..67144486. E2 has retired; successor E5 (session_01QsZymCraDjLzVDooLvigNk).
- Rewiring: a seeded wire order per job (key 1016, `j.order`, older jobs fall back to chart order) and the right terminal is the wire's chart position (rewRight), so the chart must be read; one faded colour (lead 17); the extra worksSideXp gone; junk j.pairs/j.wrongs defaulted; rewBoxes skips a junction with an open job.
- Favour cases: FC_TIER = 3 (friend, lead 17); 'fcase' in WORKS_SIDE_KINDS; the side job is finished (jobFinish) when solved, no board turn-in; an accepted favour's expiry is pushed out 14 days (no lapse mid-case) and a lapse closes its side job.
- Tickets: a wrong call is a fitted call that didn't fix it (`c.fits > 0 && !j.workDone`), so notepad crosses and "talk it through" no longer count; flag ticket.solved set in ffGrade; the toast split in two (Calder's line, then the pin).
- Leak +1 in total and the worn-joint chore's J.xp = 0: settled by E1's 0.45.11 turn-in (side kinds flat, j.xp === 0 skipped).
- **Fix (done in E5's 60a418fe): the pin still never shows.** ffPin still needs `playerRigRebuild`, which no branch defines; lead 17 ~06:05 made it E2's (now E5's). Build it (rebuild the player's rig from PLAYER_SPEC, disposing the old meshes, no R()) and a check that the pin appears after ffGrade(1) and survives a reload.
- **Cross-seat (E1's to fix, see E1's verdict): rewiring's right-first-time +1 is now paid by nobody.** The m15 page says +1, +1 more right first time; E2 rightly dropped its own payment (lead 17: right-first-time stays with E1's turn-in), but E1's 0.45.11 made side-kind turn-ins flat, so j.rightFirst is ignored for 'rewire'.
- Note: the wire-order draws use indices k*8+10+i under key 1016, which overlap the next day's chart draws (k+1)*8+2+i: correlated, harmless.
- Checks on 67144486: queued (and on a merge with E1, for the side save part).

### W2 claude/writer-p5 0e8571a (0.48.116, ticket.nohint for E2), R5: PASS
Same words as E2's fallback in caseHint. Bakes 9560 lines; lines_check PASS. W2's tip.

### W2 claude/writer-p5 4e0d212 (0.48.115, 24t lines matched to the code), R5: PASS
cabin.spot.rug/desk/shelf/ledge are now the placing sentences; star.title/pick ({a} {b})/right ({star})/wrong (look again)/name ({n})/done (ten stars) match every worksText call in d51c5edf; the unread cabin.item.* go. Bakes 9559 lines; lines_check PASS. This settles fix 4 of E3's 0.53.7 on the writer's side (E4 still checks the code side). W2's tip.

### E3 claude/mech-diagnose d51c5edf (0.53.8: R4's two M10 fixes; same game as WIP 95d3737a), R5: PASS
- Fix 1 done: shopFetch with an empty shelf keeps j.parts and sets j.offcuts, then ticks the fetch stop, so the make stop stays (mech_check: an empty shelf ticks the fetch only). The make stop takes the part from your hands only if you have it, so stores never go below 0.
- Fix 2 done (the lead's call, in person): the finish hold puts the thing in SHIP.player.carry (refused at the start if your hands are full); "Give the <thing>" shows only while you hold it, and handing it over takes it from your hands; a made order not in your hands (old save, reload, put down) is given back at the order board; main storage won't take it.
- shopData now cleans xpDay/taught/posted and an order's day/job/part (R4's note).
- Note (small exploit, no fix asked): the order thing "mug rack" has the same name as TINKER_LIST's mug rack (a SOC_GIFTS gift and a cabin ledge thing in 24t), so the order's rack can be given as a gift to anyone or put on your cabin ledge; the board then hands you another. Renaming the order's thing (W2's thanks line names "mug rack") or marking the held order thing would close it.
- Checks: running (mech_check, deck_check, interactions_check, cadet_test vs 626a907c).

### E3 claude/mech-diagnose 2ce8e9e7 (0.53.7, 24t cabin touches and star logging), R5: PASS WITH FIXES (five; E3 has retired, so for E3's successor)
Read with a helper agent against off-shift.html; 1-3 confirmed by hand.
- Good: one owner (24 new CABIN_*/CAB/cabin*/STAR_*/star* names, none elsewhere; calls playerBed()/worksHome(), no copies). Keys 1024/1025 via schedU, no R(). Saved in side.cabin / side.stars, cleaned on read, defaults. E1's cad17046 reads W.ms 'stars', which E3 pushes. Stars give friendship only (no rep). Phones: dressMat/col(), each spot one merged mesh (max 4 draw calls), +.002 off the surface, the rug's underside at .012, disposed in unloadDeck. Star logging 20:00-23:30 from Day 6, room J on Deck 2, one a night.
- **Fix 1: the shelf thing floats.** cabinSpots 4-23 shelf at [40.2, 2.17, 10.2] (7363) is past the end of the 4-23 keepsake plank (placeWall 'n' at .5, 0.92 wide, about x 39.04-39.96). Move the spot onto the plank or draw a small bracket shelf there.
- **Fix 2: some shelf things are invisible.** CABIN_FITS.shelf has 'paper novel', 'puzzle book', 'pocket puzzle', 'metal puzzle'; CABIN_LOOK has none of them, so they leave your hands, count as a touch and draw nothing. Add their looks.
- **Fix 3: cabin spots work from anywhere.** cabinTap (40849) never calls approach(); every other tap (starTap too) walks you there first.
- **Fix 4: text keys don't match W2's step4.lines.** cabin.spot.<k> is read as the placement sentence but W2's are spot labels ("Rug"), and .desk/.ledge don't exist (W2 has .lamp/.plant); star.done is read as the ten-stars message but W2's is "One a night. The sky will keep."; star.wrong says "try again tomorrow night" but you can retry at once; star.pick has no {a}/{b}, dropping the chart's two stars. Agree names with W2 (e.g. cabin.put, star.ten).
- **Fix 5 (the brief): mech_check has no real save round trip**, and its star part copies the relAdd logic instead of driving starLog/starTap (one a night, the hours and the Record line at ten untested).
- Notes: cabinPlaced isn't wired into lockerTidy and visitors' cabin.remark isn't built (page items: the lead's call whether they wait); cabinMood's +4 leisure is 24t's own 06:00 tick (hook register) and CAB.woke isn't saved (a reload at 06:00 can repeat it); on an observatory-night evening the first telescope tap opens the star log, not the tradition; the ledge plank is drawn only when something is on it, in the thing's colour; CABIN_FITS repeats TINKER_LIST's cabin field; E1 shows "Star logger, Day {n}" vs W2's works.ms.stars "Star logger".
- Lead 17 ~06:06: E4 (session_01PtXCwVBprdkJ6AcQisEyJq) owns E3's code and does these five first; lockerTidy and cabin.remark come after M17 (or in 0.63.5).
- Checks: on d51c5edf (contains it), running.

### E2 claude/mech-incidents 3014b864 (0.51.10: R4's three fixes on 0.51.6, the pin, the ticket hint guard), R5: PASS WITH FIXES
Diff 51611e02..3014b864 (18 game lines, a mech_check save part).
- Done: R4's fix 1 (the flush penalty uses N.stage, the stage of that harvest's job, saved and cleaned); fix 2 (mech_check `side` part: leaks, nozzles, rewire, favours and ff through a real saveGame and reload; on E2's branch alone it prints "not checked" because worksClean there doesn't keep `side`, so it proves itself only on a merge with E1); the ticket hint guard is one line in caseHint (c.ticket, under 3 clues: ticket.nohint); the pin is one line in section 8's builder (`s.pin`: a gold cylinder merged into rig.chest, right breast, no extra draw call; the gold is a literal colour like the rest of that builder).
- **Fix A: two things lean on E1 code that doesn't exist on any branch.** (1) The worn-joint chore now sets `J.xp = 0` ("24 core skips j.xp === 0"), but E1's turn-in (mech-rounds 39740) never reads j.xp: it still pays WORK_XP||1 outside the cap. (2) ffPin still needs `playerRigRebuild` ("24 core's"), which no branch has, so the pin still never shows. Either E1 adds both (the lead to confirm with E1) or E2 does it locally (e.g. 'joint' through the cap, or not posting it as a paying chore; a rebuild path for the player rig in E2's own block, if the lead gives E2 that function).
- **Fix B: a leak still pays 2, not the lead's +1.** leakDone (42158) still sets `j.foundBy = 'you'`, so E1's turn-in pays 1 + 1 (found). Drop the foundBy (keep e.found for the record), so a leak is +1.
- Still open from 0.51.7/0.51.8/0.51.9 (sent after this hash was made): rewiring's three, favour cases' three (and the friend tier), tickets' 1 and 4 (a crossed-out suspect = a wrong call; flag ticket.solved).
- Lead 17 ~06:05: the j.xp === 0 skip is E1's (fb499eb, 0.45.11); playerRigRebuild is E2's (E2 owns the pin); E2 makes a leak +1 in total.
- Checks on 3014b864: queued.

### E2 claude/mech-incidents 51611e02 (0.51.9, 24l fault-finder tickets), R5: PASS WITH FIXES (four)
Diff d0e6fe99..51611e02, read with a helper agent; fixes confirmed by hand.
- Good: Calder's Mail Day 13 on (mailSend); a ticket at 08:00 on a workday of yours, slot 23, held to 17:00, until graded; the case engine only called (caseMake/caseShow/caseRelease/caseTalker/caseKindsOpen/caseCauses); keys 1022/1023 via schedU, no R(); saved under side.ff, cleaned, the ffOk marker not enumerable. One owner: FF_*/ff* names nowhere else. Rep only through the normal turn-in (no worksSideXp, no double pay). Line keys exist with fallbacks.
- **Fix 1 (bug): a crossed-out suspect counts as a wrong call.** 42044/42050 test `c.crossed.length`, but crossed also fills when you cross a suspect out on the notepad (40880) and with "talk it through" (40821). Normal deduction ends the ticket "Not yet. Next week." Test the calls instead (a call that isn't c.cause).
- **Fix 2 (the lead's call): "hints only after your third look" isn't built.** FF_HINT (41982) and c.ticket (42013) are read nowhere; caseHint has no ticket guard. One guard line in caseHint (H2's function: one-line hook, say so in the row).
- **Fix 3: the pin can never show.** ffPin needs `playerRigRebuild` (no branch has it) and section 8's builder has no `s.pin`, so it always returns false (and is retried every tick). The lead's call: a small gold disc baked into the chest on the right breast (merged, col(), no extra draw call, no R()), drawn from spec.pin, with a rebuild path that exists; old saves without a grade: no pin.
- **Fix 4: Calder's line never plays.** calder.lines:635 needs `flag:ticket.solved`; nothing sets it. Set it in ffGrade.
- Also (small): no real save round trip of side.ff in mech_check; the toast joins ticket.solved and works.pin into one odd sentence ("... Calder's initials on it. your fault-finder pin"); 'ff1' goes into W.ms but the Record shows only 'commissioned'; "one more clue" for the ticket's case isn't built (c.ticket set after caseMake); after a 17:00 release, check the ticket's case doesn't stay in C.open.
- Checks on 51611e02: queued.

### W2 claude/writer-p5 1beddb1 (0.48.114, rewire.faded singular, the lead's m15 call), R5: PASS
"This one's faded. Which colour was it?" Bakes 9564 lines; lines_check PASS. W2's tip.

### E2 claude/mech-incidents d0e6fe99 (0.51.8, 24l favour cases), R5: PASS WITH FIXES (three)
Diff dd0ec462..d0e6fe99, read with a helper agent against favour-cases (D3's answer de012aae); fixes confirmed by hand.
- Good: the six cases (lamp, cold, squeak, shower, clock, speaker), three clue looks then "What's causing it?" from three suspects shuffled per favour (key 1020), a wrong pick never fails. Day 13 on, not juniors, once a week at an evening minute, the friend's Mail, offered (not on the board), lapses after 3 days. Calls section 17's favourPost/favourById and the social chat hand-back; no copies. One owner: 18 new FAVOUR_CASES/FC_*/fc* names, none elsewhere. Keys 1019-1021, no R(), no meshes. Every line key exists on writer-p5 (with fallbacks).
- **Fix 1 (the cap):** no `WORKS_SIDE_KINDS.add('fcase')` (24o/24q/24r each have one, e.g. 42082). The 'fcase' turn-in pays worksXp outside the +2/day cap, on top of the favour's own hand-back rep. Add the line after the jobKindAdd (41945). Better (the page: "hand it back in the chat card"): finish the side job with jobFinish when the case is solved, no Works-board turn-in.
- **Fix 2 (bug):** an accepted favour still lapses at `expires` (section 17, 16790: `!j.workDone`), set at the ask (41916). Mid-case it lapses ("asked someone else" after you said yes) and the 'fcase' side job is left in your jobs for good. When the side job is made, push F.expires out (or null); in the lapse branch also close any `kind 'fcase' && favour === e.id` job.
- **Fix 3 (the brief):** a real save round trip of side.favours, the side job and F.fcase (mech_check only cleans junk in memory).
- Notes: "friendly or better" is `relTier >= 2`, but REL_NAMES[2] is 'colleague' (friend is 3): which was meant? Not built from the page: a weekend ask, a person as a clue, the occasional thank-you gift; W2's favour.thanks / favour.head / favour.<id>.ask are never read. The lamp lines name Pell's guitar next door, but Pell can be the asker.
- Checks on d0e6fe99: mech_check OK (fcase part), social_check OK, cadet_test vs dd0ec462 ALL IDENTICAL (renderer noise only).
- Lead 17's calls after this verdict: "friendly or better" = the friend tier (relTier >= 3), as a named constant.

### E2 claude/mech-incidents dd0ec462 (0.51.7, 24q M15 rewiring), R5: PASS WITH FIXES (three)
Diff b6130f62..dd0ec462, read with a helper agent against m15-rewiring; the fixes confirmed by hand (line numbers in dd0ec462).
- Good: weekly at 08:00 on a workday of yours (not the incident/leak/test day) from Day 17, Tier 2 on the job; a wrong pair re-opens only its stop (never a fail); faded charts from 3 uses with the lights first; left alone it's held to 10:00 next workday, then the crew take 45 min. Calder's demo on 4-junction-2 (the officers' corridor closet, the lead's call); yours is 4-junction-1. 'rewire' in WORKS_SIDE_KINDS (after E1's core, no TDZ). One owner: the 19 REW_*/rew* names are nowhere else; no m15 ladder push (E1's row matches, ROW_AGREE). Keys 1016/1017 only, no R(). No meshes. Every line key exists on writer-p5 (rewire.*, wire.*, train.m15.calder). node --check OK.
- **Fix 1 (double pay):** rewDone (42108-42109) sets j.rightFirst AND calls worksSideXp(1, 'rewire'); E1's turn-in already adds +1 for j.rightFirst. Today the +2 cap hides it. Delete the worksSideXp line, keep j.rightFirst.
- **Fix 2 (the brief):** a real save round trip: mid-job (after a wrong pair) saveGame/loadGame, check pairs/wrongs/the open stop survive and side.rewire reads back. Default j.pairs/j.wrongs where read (an old/junk job makes `j.pairs[k] =` throw and `j.wrongs +=` NaN, 42093).
- **Fix 3 (gameplay):** the right answer is always the stop's position: wire stops go in chart order (42078) and the options are T1..Tn in order, so the k-th wire is always Tk (42092) and the chart never needs reading. Store a seeded stop order on the job at posting (key 1016) and check the colour's chart position.
- Notes: the code fades two colours, the page says one: lead 17 ~06:02: ONE (the page); W2's line is singular in 1beddb1. rewBoxes can pick a junction with an open section-17 repair (two jobs on one box). On E2's branch alone nothing posts until E1's core is merged.
- Checks on dd0ec462: mech_check OK, cadet_test vs b6130f62 ALL IDENTICAL.

### W2 claude/writer-p5 1c051274 (0.48.113, M13/M14 lines matched to E2's code), R5: PASS
leak.turning, leak.tight, noz.plant and the meeting train.m13.calder added; leak.look.wall/floor/colder and leak.hint go (E2 reads none of them). Fresh archive: content_gen bakes 9564 lines, 48 meetings; lines_check PASS (the 2 old warnings). W2's tip.

### W2 claude/writer-p5 d1e62d3 (0.48.111, favour.call and favour.not for E2): PASS
Bakes 9564 lines; lines_check PASS. W2's tip.

### E2 claude/mech-incidents b6130f6 (0.51.6, 24o M13 leak hunting + 24r M14 irrigation + the one-owner rows): PASS WITH FIXES (three)
E2's own diff: 7f66f124..b6130f6. Read with a helper agent against m13/m14; the fixes below were confirmed by hand.
- Good: M13 is weekly at 08:00 on a workday you're on shift, from Day 12 (keys 1013/1014): puddle, then damp, then the joint (turn, or replace if worn). Galleries after 3 leaks of yours; the crew take the long way. M14 is the first harvest Saturday from Day 13 (the lead's call), 2-4 nozzles, a hold per rack, bonus up to 0.1 on the next harvest. Saves: side.leaks (the last 12) and side.nozzles are under SHIP.works.side, cleaned on first read, defaults when missing. No R(). One owner: none of E2's 42 new names is anywhere else; the CAREER_LADDER pushes are gone; ROW_AGREE is in mech_check; 'leak' and 'nozzle' are in WORKS_SIDE_KINDS. Section 16's harvest hook is typeof-guarded and exactly x1 with no bonus (food_check OK). Phones: puddle and damp decals are offset from the floor and wall (not coplanar), colours go through col(), one InstancedMesh each, disposed.
- **Fix 1 (bug): the flush penalty uses the wrong stage.** nozPost (~42056) works out the last harvest's bonus with `worksStage('m14')` *now*. When the stage went up after the last job was posted (at stage 0, with no flush stop), the next harvest gets x0.8 for a flush you were never offered. Use the job's stage (j.stage is stored; keep it in N).
- **Fix 2 (the brief): a real save round trip.** mech_check's m13/m14 parts clean junk in memory but never save side.leaks / side.nozzles through the game's save and load them back.
- **Fix 3 (the cap): one leak can pay twice.** leakDone (~41959) sets foundBy 'you' (turn-in 1+1, capped). A worn joint also posts jointJobPost with foundBy 'you', and that chore's kind isn't in WORKS_SIDE_KINDS, so it pays another ~2 **outside** the +2/day cap. Put the joint chore through the cap (or don't mark it foundBy). The page's "+1" vs 1+1: lead's call.
- For W2: E2 reads keys W2 hasn't written: leak.tight, leak.turning, noz.plant, train.m13.puddle, train.m14.rack (all have fallbacks in code). W2 has keys E2 doesn't read: leak.look.wall/floor/colder, leak.hint. No train.m13.calder meeting (Calder is in LEAK_BY).
- Notes: stage 3 of M14 is a look plus machineFound, not "service the irrigation machine"; the kit's "damper this way" only shows at the puddle, from stage 1; the first leak skips leakDay's exclusions; if an open leak's job ever disappears, leakOpen() blocks new leaks for good; nozState() writes a default side.nozzles from inside the galley step on a harvest day.
- Merge note for BM7: mech_check.py conflicts with E1 b82c8e2 at the same place after part_m9 (E2's M13/M14 parts vs E1's SIDE part): keep both. The html merges with E1 and E3 with only the build lines; `node --check` passes.
- Checks on b6130f6: mech_check OK, food_check OK, cadet_test vs 7a6e137 ALL IDENTICAL.

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
