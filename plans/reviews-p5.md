# Pillar 5 reviews (reviewer R, session_01MSLjUdmeVJetxFhh9PqzLt)

How: behaviour, save and schedule changes in depth (against the piece's approved page in plans/mechanics/ on claude/p5-design, determinism, old saves load, phones first, cadet_test differences explained); content and test-only changes skimmed. Verdicts newest first.

## Passing tips
- H claude/mech-cases **eece4d4** (0.55.0)
- W claude/writer-p5 **843bac9** (0.48.84, text; with LOWs)

## Verdicts

### W 843bac9 (0.48.84): Pillar 5 text batch 1 — PASS with LOWs (skimmed: content only)
- Own commits only (18b4fa2, 843bac9 on writer-0607 0cc4cdf): content/works/*.lines, keys-p5.md, four train.* meetings, calder/torres-zeke `work` lines, facts.md row, lines_check placeholders. No game code.
- Checks (my run on 843bac9): content_gen bakes clean (20 meetings); lines_check PASS (0 errors, 2 old warnings).
- LOW 1 (design clash, for the designer and lead): the roster has Torres off Thursdays and Fridays (`offDays [3, 4]`, 0 = Monday), but m7-scanner.html and p3-whats-been-tried.html say Torres teaches both on Day 5 (Friday) and does the fallback tries "on Day 5 at 07:00-08:00 (he's on shift Fridays)". The writer wrote Calder as teacher with Torres variants, which fits the roster; the pages (and C/H's code) need to agree: pick the teacher by who's on shift.
- LOW 2: `case.solved` "Solved. Fetch the {part} and fit it." If it shows at Call it, "Solved" gives away a right call before the fit (the page: right or wrong is learnt at the machine). Reword ("Fetch the {part} and fit it.") or say in keys-p5.md it shows only after the fix works.
- LOW 3 (designer's page, not the writer): p3-whats-been-tried.html's puzzle_check line still says "the first case is Deck 4's lights on Day 5"; the page's own first case is Washer 2.

### H eece4d4 (0.55.0): device chips block + puzzle_check part 1 — PASS
- Matches case-engine.html "Fault notes on the device": `{ kind: 'chips', items: [{ label, on, action }] }` in section 19's skin, big toggles (48px, over the 44px floor), crossed out (struck, dim, dashed) only while `on === false`, `aria-pressed`; `devChips()` falls back to a buttons block with "✕ " on crossed ones when `DEVICE_SKIN.has('chips')` is false. Nothing uses it yet.
- Page elements only: no 3D, no draw calls, no R(), no save or schedule change.
- Checks on eece4d4 (my run): cadet_test vs d3d720b ALL IDENTICAL; device_check OK; puzzle_check OK (chips 48px high, tap runs the action, fallback labels and taps right).
- Note for the combine: the HUD/GAME_BUILD reads 0.55.0 (seat series rule); the build master sets the candidate's number.
