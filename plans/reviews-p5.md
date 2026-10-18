# Pillar 5 reviews (reviewer R, session_01MSLjUdmeVJetxFhh9PqzLt)

How: behaviour, save and schedule changes in depth (against the piece's approved page in plans/mechanics/ on claude/p5-design, determinism, old saves load, phones first, cadet_test differences explained); content and test-only changes skimmed. Verdicts newest first.

## Passing tips
- H claude/mech-cases **eece4d4** (0.55.0)
- W claude/writer-p5 **0d179ac** (0.48.86, text; contains 843bac9 and 76fc413; no LOWs open)

## Verdicts

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
