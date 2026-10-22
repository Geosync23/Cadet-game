# Review: controller support, second reviewer (RV2)

RV2 (session_01E1TTHbhLzy2U6pAoGh7E9a), branch `claude/review-controller` (notes only; the game is never changed here).
Lead 25 (session_01J2aTyEohBf8KFHCsTqt3LW); team leader CT1 (session_019sqDowb6QNf3KZAYMSx1jM, claude/controller);
first reviewer PR9 (session_01B1FUTc4sJR4Q5FFnx7L6Db, notes on claude/review-8, `plans/review-9.md`).

## Split (proposed to PR9, 2026-10-22)
- PR9: the foundation (section 26, the switch, polling, connect/disconnect) and packages p1-p2.
- RV2: packages p3-p5 and CTT's `controller_check.py` (the fake pad, the reachability sweep, its mutants).

## The bars (PR9's, `plans/review-9.md` "What I'll hold the turns to")
No pad = identical (cadet_test ALL IDENTICAL, switch off and on, pad present but never pressed); nothing made at load;
no `R()`; the save byte-identical with no settings changed; touch-after-pad identical (no stray focus outline, marks
or ring); the ring not coplanar, through `col()`, one draw call; a reachability sweep that lists clickables from the page,
not from the controller's own panel list; A on the deck = tap() by state after; stick walking through `player.steer` in
all four turns; keyboard unchanged; disconnect rules; check_fast and names_check.

## Per package
For each branch `claude/controller-pN` as it lands: adversarial read of the diff (`tools/section.py --diff`), cadet_test
against its base (no pad: ALL IDENTICAL), check_fast, the relevant controller_check parts, planted mutants
(`plans/review-controller/mutants.py`). Verdict PASS / PASS WITH FIXES / FAIL to the builder, CT1 and the lead.

(No package has landed yet.)
