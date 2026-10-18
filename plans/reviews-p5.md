# Pillar 5 reviews (reviewer R, session_01MSLjUdmeVJetxFhh9PqzLt)

Who gets verdicts (lead 11, 09:27; kept by lead 12, session_01GjWhU9Z9V8RNoR8yyELA9V, from 10:14): PASS → the seat and BM4 only; FAILs and design clashes → also the lead.

How: behaviour, save and schedule changes in depth (against the piece's approved page in plans/mechanics/ on claude/p5-design, determinism, old saves load, phones first, cadet_test differences explained); content and test-only changes skimmed. Verdicts newest first.

## Passing tips
- C claude/works-career **d518673** (0.44.9, contains 87df8f5..ae6598a; 1 LOW open)
- A claude/deck-0607 **6cc826b** (0.47.2, contains c20f91f and ad5e704; no LOWs open)
- H claude/mech-cases **171f901** (0.55.11, contains everything from eece4d4; no LOWs open)
- W claude/writer-p5 **0d179ac** (0.48.86, text; contains 843bac9 and 76fc413; no LOWs open)

## Verdicts

### C a8dd78e (0.44.8) + d518673 (0.44.9): fixes for item 1 and the LOWs — PASS with a LOW (read; C's checks)
- Item 1 closed: trainOffer sets cur.told = false and tells at once in play (trainTell: a toast and the goal arrow). Asked while you slept, trainTick tells you the first minute you're up, while the meeting is still ahead. `told` is cleaned on load. LOW 2: a 'held' cur from an earlier day ends (trained) at the next workday's ladderTick. LOW 3: act('open') takes a tab, plus worksTabShow(id). LOW 4: no sub-block reserve and no machine kind → trained at the meeting, with no stand-in fault. Nits done (851 documented; the sub-block data rule; small rows train only once opened; WORKS_TAB reset). a8dd78e: WORK_MECH[id].at(day), a meeting's earliest minute (M1's m4 after the unload), capped sensibly.
- LOW (new): trainTell's toast text is "a Mail from the same sender within a day". On Day 5 that can be Halloran's 08:05 "Board, when you're in" Mail rather than the training ask. Match the Mail by its subject, or keep its id on cur.
- C's checks: career_check OK (asked during skipTo → told false; first tick → told true, goal set), mech_check OK, cadet_test ALL IDENTICAL. Not re-run by me (my browser queue is on P and S).

### H 171f901 (0.55.11): `verbs: 'case'` on the Fault notes tab — PASS (read; H's checks)
- One field on the worksTabAdd call, so C's `split(':')[0]` routing sends 'case:*' to the tab whichever tab is on show. H's checks: puzzle_check OK, cadet_test ALL IDENTICAL.

### C 87df8f5 (0.44.0-0.44.6) + ae6598a (0.44.7): section 24 WORK core — FAIL, one item (in depth; read with a helper against foundation.html)
- **Item 1 (blocking): a big row's ask is silent when you've slept, which is the usual case.** Big rows open from 06:00 (WORKS_ASK [360, 630]). Sleep skips to 07:40, so SIM_ADVANCE's handler (line ~34879) runs ladderTick for 06:00 and 07:00 during the skip. trainOffer (34626) then sends the Mail `quiet: true`, and its toast and setGoal need `t >= shipNow() - 1`, which is false. So on Day 2 you wake to a silent Mail about Rounds: no toast, no goal pointer. The page says a toast, a Mail and the pointer. Fix: keep `c.told`, and in play (trainTick or the minute tick) give the toast and setGoal the first time `st === 'meet' && !c.told`. Or open a big row only in play, not inside SIM_ADVANCE, while its meeting is still ahead.
- LOW 2: a `held` escort can stall the ladder. worksDone sets st 'held'; only worksEscortEnd or caseCalled clears it. While W.cur exists no big row opens, and the re-offer path handles only 'ask'/'again'. If Day 5's case is never called (or 24k is missing), m7 is never trained, and m6 and t2 never open. Fix: a `held` left from an earlier day trains you (worksTrained) or drops the hold on the next workday.
- LOW 3: the Works app can't open on a given tab. act sends every verb, 'open' included, to the tab on show, so H's `deviceNotify({ app: 'works' })` for a new clue opens on whatever tab was last shown. Let 'open' take a tab id (action.arg) or add worksTabShow(id).
- LOW 4: the default training reserve (trainDo → jobReserve(row.job, ...) with 'round'/'tune', which aren't machine kinds) falls back to the first free Deck 4 machine and makes it faulty, often the one the teacher just fixed. Make a sub-block's `reserve` required, or refuse the default.
- Note for H: the fallback verb routing matches `verbs || id`. H's tab is id 'faults' with no `verbs`, so 'case:*' only reaches it while Fault notes is on show. That's fine today, since the case buttons are only there, but add `verbs: 'case'`.
- Nits: the comment at ~34441 says 851-854 are spare but worksNext uses 851. DEV_NOTES says worksTick (it's worksCareerTick) and leaves 'held' out of cur's states. worksClean drops unknown keys, so a sub-block must keep its own SHIP.works data via its own save reader, as 24k does; put that in the hook register. worksUse trains a small row that never opened. WORKS_TAB isn't reset on a new game.
- Correct to the page: no R(), Math.random, Date.now or performance.now; schedU keys 850 (the meeting time) and 851 (What's next, display only). SHIP.works is null till worksInit, cleaned once from the save (v 1), with every field clamped, old or junk saves → null, SAVE_EXTRA, reset on newGame. Ten rows, days, sizes and needs as the page; m7/p3 by ['torres-zeke','halloran-emeka','calder'], first on shift wins; at most one big and one small a workday, nothing on days off; the training flow; toolGive; worksIsOpen = the row has opened (FAQ). Bands new/steady/reliable/trusted/relied, 'New officer' after a promotion; skillWord at 5/15 (P's careerSpeed reads sk). worksTabAdd is a hoisted function with a var list: safe whatever order 24k loads in. 73 new top-level names, none clashing; worksCareerTick and WORK_RANKS avoid section 17's worksTick and RANKS. No 3D, no draw calls. Inert before SHIP.works, and with WORK_MECH empty nothing opens.
- Checks: C's (cadet_test ALL IDENTICAL, career_check, mech_check); not re-run by me yet (my browser queue is on P and S). I'll re-run them on the fix.

### H 55343c6 (0.55.10): the teacher stays for Day 5's case — PASS (read; H's checks)
- One guarded call, `worksEscortHold('m7')`, only when Day 5's m7 job is the Washer 2 training case. It matches C's ae6598a (worksEscortHold sets c.hold; 24 core ends the escort on caseCalled) and the designer's 6fb5c49. H's checks: puzzle_check OK, cadet_test ALL IDENTICAL.

### H 9cb6425 (0.55.9): fallback when S's jobSetPart refuses — PASS (read; H's checks)
- caseCall, scanPick and scanFitted now set j.parts themselves when section 17's jobSetPart returns false. That happens on a job whose parts are empty, which a case's job is after caseShow. Without it the call set no part on S's real build. Three one-line edits, correct.
- H's checks: cadet_test vs d3d720b ALL IDENTICAL; on a trial combine with S 96cf5cb + C 2ea7ab2, puzzle_check (no stand-ins) and machine_check OK. Not re-run by me (my browser queue is on P and S).

### H a07692b (0.55.8): batch 2's LOWs — PASS
- One P3 note on the job, the rest on the machine's panel (`at: i && pp`): LOW 1 closed. Day 5 skips Washer 2 only if your own wash is in it (SHIP.clothes.hamper at that washer), as well as a job you've claimed there: LOW 2 closed. j.scanWorn dropped (an old save's leftover is ignored).
- Checks (my run): cadet_test vs d3d720b ALL IDENTICAL; puzzle_check OK.

### A (DA4) 6cc826b (0.47.2): the kits merged into each deck's static geometry — PASS
- wallFixed() builds the five kits into staticRoot in materials the decks already draw (M.slateDark, WM.steel, WM.red). There are no canvases and no P5KM. They stand on the floor (legs, posts, pedestals), so they don't hang in the air when the walls lower. Only the extinguisher is its own mesh (noMerge, for drillExtShow). Valve ticks at z .071 sit 6 mm proud of the strip (.065). The floor pads' undersides touch the floor but face down (culled), as elsewhere.
- Draw calls by the lift vs d3d720b: Deck 3 226 (+0), Deck 4 186 (+0), Deck 5 179 (+1). Memory: Deck 4 steady at 373 geometries and 39 textures, the same as the base.
- cadet_test vs d3d720b: 12 shots differ on Deck 4, all by the junior corridor's valve rack. It now stands on the floor where the near wall is cut away, so it shows in the opening views; I checked a_start by eye. It sits at x 5.15-6.85 on the corridor's north side, clear of the washroom door (column 3) and Bunk 1's door (column 8). i_tap3/i_tap4 differ by 5 px (renderer noise). State differs only by items, memory, calls and triangles. deck_check OK.

### H 18c5cee (0.55.6) + 9200b70 (0.55.7), with e46c8bb (test only): the scanner on head-scratchers — PASS with LOWs (item 1 closed)
- Per designer 1d87fc6: on a job with a case, every suspect's part reads 40-60 and the rest 70-96, from the same hash with no link to the cause. puzzle_check swaps the cause and gets the same readings. Day 5's training case is fixed at pump 55, seal 44, valve 49, so the cause never reads lowest. j.scanWorn is gone. Non-case jobs keep m7's rule.
- e46c8bb: puzzle_check opens Fault notes as C's Works tab when 24 core is in (H's trial combine with C 2ea7ab2: puzzle_check and device_check OK; not re-run by me).
- Checks (my run on 9200b70): cadet_test vs d3d720b ALL IDENTICAL; puzzle_check OK (Day 5 through m7: the case shows at your reading on Washer 2, first note collected, caseCalled sent).
- Still open from the 0.55.3-0.55.5 verdict: LOW 1 (three decoys put two notes on the board) and LOW 2 (Washer 3's fallback should test your own wash).

### H 2d7c239 (0.55.3), a2e2ac6 + b5b9e52 (0.55.4), 47fc193 (0.55.5): scanner 24g, P3 and Day 5's case, LOW fixes — FAIL, one item (in depth)
- **Item 1 (blocking; the designer's ruling 1d87fc6, after these commits):** on a job with `j.case` set, scanRead still uses m7's normal rule. The cause reads 12-35 and a worn decoy 40-60, so the lowest bar always names the answer and the scanner settles every head-scratcher. puzzle_check even checks it: Day 5's case reads "pump failing, seal worn". Build 1d87fc6's rule: on a case job every suspect's part reads 40-60 ("worn"), hashed from schedU(machSeed, day, 875) with no link to the cause; non-suspects read good; the reading is not a clue for the solver. Day 5: pump, door seal and drain valve all read worn (j.scanWorn goes). Change puzzle_check's Day 5 arm to match, and add an arm: on a case job no reading tells the cause apart.
- Otherwise to the pages. Scanner: 3-5 parts, frozen j.scan, worn decoy only with the same card and a different sign, wrong pick → the part back on its shelf (Tier 1), the job names the right part, tool wear +.01 a reading, keys 874/875. P3: one try per decoy by Works crew really at work 2-12 h after posting (else a hand next morning 06:00-09:00), the part off its shelf, notes killing only their decoy, shown inside your shift. Day 5: staged 18:00 Day 4 on 4-washer-2 (pump), held in slot 20, and per 6fb5c49 your m7 reading on Washer 2 opens it with the teacher beside you (c.m7, caseCalled note for 24 core's escort).
- Batch-1 LOWs, all handled. Re-call before fitting replaces the call (c.fits). Waiting cases end (3 days; a training case at the reserve's until; taken early → a plain repair). The talk toast names c.by. case.title, chief.p3.N and fault.tried come through worksText with stand-ins. The stand-in app is `faultnotes`. LOW 4's carried part is left to P's shelves (agreed).
- Checks (my run on b5b9e52): cadet_test vs d3d720b ALL IDENTICAL; puzzle_check OK; device_check OK; machine_check OK; player_check OK. H reports 47fc193 cadet_test ALL IDENTICAL, puzzle_check and device_check OK.
- LOW 1: with three decoys p3Tries puts notes 0 and 2 on the board (`i % 2`), but the Chief's note says "One's on the job; the others are on the machine". Put only the first on the board.
- LOW 2: p3Stage moves to Washer 3 when you have a job claimed on Washer 2. The page means your own wash in it (`SHIP.clothes.hamper.at === 'washer' && .washer === id`, as washerBusyUntil reads).
- Nit: the readings' key 875 is used with the same (machSeed(m.id), d) for both the training cause pick and the worn-decoy pick, so the two are correlated. Harmless.

### A (DA4) ad5e704 (0.47.1): shared kit materials, the valve strip moved — PASS
- P5KM: the kits' materials and two painted labels, made once at load (line 7460, before the first buildDeck, no R()). Their ids are below every deckMark, so unloadDeck leaves them alone (no blank labels on a revisit). Deck 4's memory holds steady over round trips (373 geometries, 41 textures).
- Draw calls by the lift: Deck 3 230 (base 226), Deck 5 184 (base 178), now in the DEV_NOTES rows. The valve strip is at z .036, 6 mm clear of the backing. Both LOWs closed.
- Checks (my run): cadet_test vs d3d720b: every shot identical; state differs only by the new kits. deck_check OK.

### A (DA4) c20f91f (0.47.0): the Steps 1-2 places and five wall kits — PASS with LOWs (in depth: geometry)
- Places: drill (5-drill-*, 5-muster-1..6, DECKS[5].drill), inspection (4-inspect-a..h), hauling (HAUL_DROPS, 5-stock-1..4), incidents (n-valve-panel / -valve-1..3 / -wet-1..2 on Decks 3-5 with DECKS[n].valveLine and .wet, 5-lift-brake, 3-extractor-alarm, 3-vent-1). All type `event` with an event tag, so they're inert: nobody's plans change. Wall kits: extBracket, bulkheadWheel, valvePanel, liftBrake, alarmPanel. They're made per deck build with no R(), colours through std()/col(), and only the extinguisher is noMerge (drillExtShow hides it).
- Checks (my run): cadet_test vs d3d720b: every shot identical. State differs only in items, wallDecor, memory, calls and triangles: Deck 4's valve panel, +10 geometries and +1 texture. deck_check OK (all new places reached; the two closet places via `works: true`).
- LOW 1 (phones first): draw calls by the lift go up on Deck 3 (226 → 235, +9: the valve panel and the alarm panel) and Deck 5 (178 → 186, +8: bracket, wheel, brake, valve panel). The DEV_NOTES row explains only Deck 4's change. These are well under budget (Deck 3's check is "under 450"), but please say so in the row. Shared materials (M.* or one std per colour) would merge more of the toruses and parts.
- LOW 2: the valve panel's number strip (PlaneGeometry at z .032) is 2 mm in front of its backing plate (front face at .03). Other wall signs sit about 5 mm out. On a phone's depth buffer 2 mm can shimmer at a distance, so move it to about .035.
- Note for the mechanics seats: `works: true` is a new place field; deck_check treats it as Works-only. Whoever routes to 5-drill-breaker or 5-lift-brake must path with Works access (the hatch).

### H df7d356 (0.55.1) + 8c76b69 (0.55.2): the case engine, section 24k — PASS with LOWs (in depth)
- Against case-engine.html: posting conditions (on shift, not an event day, 06:00-15:00, jobTier <= your tier, under the open limit, a kind fits, roll key 880 < rate; senior .33 on Tier 3 machines), kind choice (881, newest-opened kind doubled for a week), eight sub-seeds (882-889), solver (exactly one left, cause never killed, fewest within the band, decks per band, every clue reachable), frozen once posted, held till shift end then released to the crew the long way, calls, wrong calls (Tier 1 part back on the shelf, Tier 2 seal/cartridge spent), talk it through after two wrong, the long way, Fault notes view (chips, clues, Where next?, Call it with Yes / Not yet), save in ship.works.cases with a cleaner. Keys 880-893 inside H's 880-894. 8c76b69: a kind opens with its ladder row (worksIsOpen, else SHIP.works.op), per the designer's FAQ.
- Determinism: every roll is schedU(machSeed, day, key); nothing calls R(); performance.now() only feeds CASE_STATS.ms. Phones: page elements only, no draw calls.
- Inert in this build: no kind registered, and section 17's caseOffer/caseFitted/heldForYou lines and FAULT_CAUSES aren't in yet (S's), so nothing changes in play.
- Old saves: no `cases` → empty; junk and a case whose job is gone are dropped (puzzle_check's junk arm); mid-case save round-trips (591 bytes).
- Checks (my run on 8c76b69): cadet_test vs d3d720b ALL IDENTICAL; puzzle_check OK (297 sweep cases, rates .10/.199/.248/.331, 0 fallbacks, 0.024 ms each); device_check OK; machine_check OK.
- LOW 1 (Step 2): the "talk it through" toast after two wrong calls names Torres for a training case (`c.train ? 'Torres' : 'Calder'`); Day 5's teacher is now Emeka Halloran (designer 210b86f, by-list first on shift). Name the case's teacher.
- LOW 2: the player-facing words are hard-coded ("Where next?", "Call it: the X?", "Head-scratcher: ...", the hints); the writer's `case.*` / `chief.p3.*` keys are in claude/writer-p5 0d179ac. Read them once baked, with these as fallbacks.
- LOW 3: a case with `wait` set is held for you with no end (caseHeld returns true while c.wait). If a kind's tries never finish, the job never reaches the crew and fills an open slot. Give it an end (e.g. release at the end of the next shift) when P3 lands.
- LOW 4 (with S's integration): Call it a second time before fitting (changing your mind) swaps j.parts and re-opens the fetch, but a part already fetched for the first call isn't put back; and it counts against "right first time". Check with S's jobSetPart/carry rules.
- LOW 5: the stand-in app's id is `faults`; the page says `faultnotes`. Trivial; it only matters to whoever looks it up.
- Combine notes (build master, C): 24 core and 24k both insert after `tilesTrophy`, before section 6: a hand merge, with 24k AFTER 24 core. 24k reads `typeof worksTabAdd` at load: if C defines worksTabAdd with `const` later in the file, that typeof throws (temporal dead zone) and the game stops loading. So worksTabAdd must be a function declaration or sit above 24k. The works app must pass `case:*` verbs to the tab's act (24k's actions use app 'works').

### W 0d179ac (0.48.86): Day 5 by Emeka Halloran, case.solved fixed — PASS (skimmed: content only)
- New train.m7.halloran-emeka and train.p3.halloran-emeka meetings (the main Day 5 version, per designer 210b86f; Halloran works Fridays) and his `work` step lines; m7/p3 panel steps renamed `hold` (seat C's step name) in Calder's and Torres's lines too.
- `case.solved` is now "Fixed. That was it.", shown only after the fix works (noted in cases.lines and keys-p5.md): batch 1's LOW 2 closed.
- Checks (my run): content_gen bakes clean (29 meetings); lines_check PASS (0 errors, the 2 old warnings).

### W 76fc413 (0.48.85): Pillar 5 text batch 2 (Step 2) — PASS (skimmed: content only)
- 23 files, text plus lines_check placeholders: seven train.* meetings (m1 m2 Torres, m3d m5 m6 Calder, m3i Tomas, m4 Yara), teachers' step lines, step2/inspect/signs/remarks lines, three incident reaction banks.
- Teachers match the pages and are on shift that weekday (roster: Torres off Thu/Fri, Yara and Tomas off Mon/Tue, Brennan off Fri/Sat): m1 Day 2 Tue, m4 Day 3 Wed, m3i and m5 Day 4 Thu (Brennan watches), m2 and m6 Day 8 Mon.
- Checks (my run): content_gen bakes clean (27 meetings); lines_check PASS (0 errors, the 2 old warnings).
- Still open from batch 1: `case.solved` LOW 2, and Halloran's Day 5 lines for train.m7/train.p3 (the lead's call).

### W 843bac9 (0.48.84): Pillar 5 text batch 1 — PASS with LOWs (skimmed: content only)
- Own commits only (18b4fa2, 843bac9 on writer-0607 0cc4cdf): content/works/*.lines, keys-p5.md, four train.* meetings, calder/torres-zeke `work` lines, facts.md row, lines_check placeholders. No game code.
- Checks (my run on 843bac9): content_gen bakes clean (20 meetings); lines_check PASS (0 errors, 2 old warnings).
- LOW 1 (design clash, for the designer and lead): the roster has Torres off Thursdays and Fridays (`offDays [3, 4]`, 0 = Monday), but m7-scanner.html and p3-whats-been-tried.html say Torres teaches both on Day 5 (Friday) and does the fallback tries "on Day 5 at 07:00-08:00 (he's on shift Fridays)". The writer wrote Calder as teacher with Torres variants, which fits the roster; the pages (and C/H's code) need to agree: pick the teacher by who's on shift. **Resolved** (lead 11): designer 210b86f makes the Day 5 teacher Emeka Halloran (works Fridays), by-list torres-zeke → halloran-emeka → calder; check Halloran's Day 5 lines in the writer's next batch.
- LOW 2: `case.solved` "Solved. Fetch the {part} and fit it." If it shows at Call it, "Solved" gives away a right call before the fit (the page: right or wrong is learnt at the machine). Reword ("Fetch the {part} and fit it.") or say in keys-p5.md it shows only after the fix works.
- LOW 3 (designer's page, not the writer): p3-whats-been-tried.html's puzzle_check line still says "the first case is Deck 4's lights on Day 5"; the page's own first case is Washer 2. **Fixed** (designer a8ec0c2). Halloran's lines are needed for train.m7 and train.p3; Calder's stay as the last fallback.

### H eece4d4 (0.55.0): device chips block + puzzle_check part 1 — PASS
- Matches case-engine.html "Fault notes on the device": `{ kind: 'chips', items: [{ label, on, action }] }` in section 19's skin, big toggles (48px, over the 44px floor), crossed out (struck, dim, dashed) only while `on === false`, `aria-pressed`; `devChips()` falls back to a buttons block with "✕ " on crossed ones when `DEVICE_SKIN.has('chips')` is false. Nothing uses it yet.
- Page elements only: no 3D, no draw calls, no R(), no save or schedule change.
- Checks on eece4d4 (my run): cadet_test vs d3d720b ALL IDENTICAL; device_check OK; puzzle_check OK (chips 48px high, tap runs the action, fallback labels and taps right).
- Note for the combine: the HUD/GAME_BUILD reads 0.55.0 (seat series rule); the build master sets the candidate's number.
