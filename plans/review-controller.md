# Review: controller support, second reviewer (RV2)

RV2 (session_01E1TTHbhLzy2U6pAoGh7E9a), branch `claude/review-controller` (notes only; the game is never changed here).
Lead 26 (session_015mHBLCf5jpnzBkFY1iBTqv, claude/lead-26; took over from lead 25 at 02:09); team leader CT1 (session_019sqDowb6QNf3KZAYMSx1jM, claude/controller);
first reviewer PR9 (session_01B1FUTc4sJR4Q5FFnx7L6Db, notes on claude/review-8, `plans/review-9.md`).

## Split (agreed with PR9, 2026-10-22 02:00)
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

## For CTT's controller_check (agreed with PR9)
The fake pad runs two ways, and both must keep the no-change rule until the first press:
(a) hidden until the first press (`getGamepads()` empty or nulls, no `gamepadconnected`): the realistic case, covering
"plugged in, never pressed = identical"; (b) present at load (a reconnect after a reload, which some browsers allow).
PR9 sends its foundation verdict first; p3-p5 build on it.

(No package has landed yet.)
