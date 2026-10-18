# Pillar 5 reviews (reviewer R, session_01MSLjUdmeVJetxFhh9PqzLt)

How: behaviour, save and schedule changes in depth (against the piece's approved page in plans/mechanics/ on claude/p5-design, determinism, old saves load, phones first, cadet_test differences explained); content and test-only changes skimmed. Verdicts newest first.

## Passing tips
- A claude/deck-0607 **c20f91f** (0.47.0; LOWs open)
- H claude/mech-cases **8c76b69** (0.55.2, contains eece4d4 and df7d356; LOWs open)
- W claude/writer-p5 **0d179ac** (0.48.86, text; contains 843bac9 and 76fc413; no LOWs open)

## Verdicts

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
