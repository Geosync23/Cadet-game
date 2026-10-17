# Review: content 5e2605e..fd3db63 (0.48.49-0.48.50), content/ only

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS** (content), with a combine rule: **0.48.50 needs dialogue
0.43.27 (c084a1a+) in the same candidate**, or lines_check fails. Four LOW wording notes.

## 0.48.49: Zeke's tour, core lines first
- `content/lines/torres-zeke.lines`: the same lines, only renumbered (no line added or lost apart from one comment;
  checked by a line-count diff). Read in the new order, place by place.
- **LOW:** works.7 "She's off today. She'll find you anyway." now comes four lines after Calder is named (works.3),
  right after the tea corner; "She" reads loosely. "Calder's off today." would keep it clear wherever it lands.

## 0.48.50: banks/missing.lines with {missed}
- **With the dialogue in 0.60.3 (0.43.23, 621a432):** I put these two files into claude/cand-0603 (0.60.3) and baked them.
  - lines_check: **FAIL, 19 errors**, all `unknown token {missed}`. So it is not harmless for the check.
  - In the game it is harmless: 0.43.23's `linesFill` returns null for an unknown token, so the line is skipped
    (`linesFill('{missed} would laugh.', ...)` gives null). Asking lineFor 296 times on day 40 for smalltalk, near,
    feel and chat never gave a line with `{` or "missed" in it.
  - So take 0.48.50 only together with dialogue 0.43.27+.
- **Tone and rules:** light, name-only (no pronouns for {missed}), no #serious, nothing in week 1 (nobody has left yet,
  so every line is skipped). No romance with the player: the partner case is plain ("I miss {missed}."), and "Sit a
  minute? That helps." is to a friend (tier>=friend).
- **LOW (facts the game may not back):**
  1. `? deck:4 time:night` "{missed}'s old bunk's still made up. Nobody's moved in yet." The condition is where the
     *speaker* is, not where {missed} slept (officers and seniors live on Deck 2), and the crew-welcome tea six days
     after a farewell brings new people who may have taken that bunk.
  2. "{missed} says the new ship's fine." and "It's only one ship over." assume they went to another ship; the
     farewell Mail only says the shuttle takes them away. Fine if the writers' bible says leavers transfer.
  3. `? place:musicroom` "{missed} used to play that one." assumes {missed} played; most crew don't.
