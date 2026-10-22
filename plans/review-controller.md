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

PR9's foundation verdict (CT1 turns 1 + 2, c99acf4f + ef59c61a): PASS (02:47). PR9's mutants: `plans/review-9/ct_mutants.py`.

## CTT's controller_check, first look (claude/controller-tests 115ee00d, work in progress)

Read in full, then run against CT1's 0.90.1 (ef59c61a) in a copy with `const PAD_BUILT = ['base', 'deck'];` added
(CT1's build has no PAD_BUILT, see 1). Early notes, not a verdict:

1. **Two controller_check.py files.** CT1's (claude/controller, 220 lines: off / quiet / base) and CTT's (671 lines)
   share a name on two branches: a merge clash, and two checks of one thing. CT1 and CTT to agree whose file it is
   (CTT's parts plus CT1's base cases folded in, I'd suggest).
2. **"not yet" passes on the real build.** CTT reads the packages from `PAD_BUILT` in section 26, which CT1's build
   doesn't have, so on the real 0.90.1 every controller part says "not yet" and the check says OK. Either CT1 adds
   `PAD_BUILT` (and keeps it current each turn), or the check finds the packages from the code (`padOn('frame'`,
   etc.). And a package named in PAD_BUILT whose part is missing from PART_FN should FAIL, not "not yet".
3. **No hidden-until-first-press mode (PR9's bar 2, agreed with PR9).** Every pad mode plugs at load (`plug` at
   DOMContentLoaded: `getGamepads()` returns it and `gamepadconnected` fires before any press): that is mode (b),
   present at load. Mode (a) is missing: slots hidden (`getGamepads()` nulls) and no event until the first non-zero
   button, then the pad appears and the event fires in that same read, as Chrome does. The idle, save and calls parts
   should run both (a) with drift (a pad in a bag) and (b).
4. **reach's touch half never leaves the DOM.** The canvas is excluded, so panels opened from the deck (the lift, a
   conversation, the job board, the crew store, the ladder, the sleep alarm, the question card, work steps, Lightdisc's
   start) are never opened, and their buttons never listed. Non-circular, but not complete. Wanted: (i) deck openers
   from cadet_test's own tap targets (a crew member, the lift door, a bunk, the job board, the store), and (ii) a
   completeness rule from the page: every element that is a panel candidate in the page as loaded (hidden and
   position fixed/absolute, or a direct child of body that is hidden at load) must be seen open in the sweep, or be in
   a short named list of "not reachable from a new game" with a reason; any other one FAILs. So a panel added later by
   another seat fails the sweep until someone opens it.
5. **The sweep's caps are silent.** MAX_DEPTH 4 and MAX_PRESSES 700 end the crawl without a word; reaching either
   should print and count as incomplete (FAIL in the pad half). And the state key includes the first 40 characters of
   each button's text, so a button showing the clock (or any live count) can make every scan a "new" state: watch
   the inventory's state count, and key on ids or the text with digits removed.
6. **touch compares the game and the pictures, not the page.** After a press and a tap it should also compare the
   PAGE_STATE (minus listener counts): `body.pad` left on, or a mark element made hidden but kept, would pass today.
   And one of the taps should be a real touch (a context with hasTouch, `page.touchscreen.tap`), the phone path.
7. The planted faults are added beside the game (their own listeners and getGamepads wrappers), not in section 26, so
   they prove each part can fail but not that it fails on section 26's own mistakes. I'll add mutants in section 26
   itself (`plans/review-controller/mutants.py`) for P3-P5.

### Runs of CTT's parts on 0.90.1 (+PAD_BUILT), each alone (scratchpad logs run1.log, run2.log)

As given (`PAD_ON = false`): idle FAIL 24, touch FAIL 12, walk FAIL 29, odd FAIL 3, unplug "not yet" (marks).
On a copy with `PAD_ON = true`: **walk OK, odd OK** (four views, half push 0.22 m / full 0.35 m, zoom to 2.4 and 0.55,
Menu / Y / View; the non-standard pad and two pads walk); touch FAIL 13.

What the failures are (all but 8.4 the check's, not the game's):

8. **The controller parts run on the file as given.** walk / odd / touch / unplug should run on the switch-on copy
   (as idle's second half and CT1's check do); on the off build they fail (walk) or pass for nothing (touch, idle).
9. **idle, "PAD_ON on, no pad": the DOM hash differs because the hash reads `<script>` text** (PAGE_STATE mixes every
   text node, the game's own source with `PAD_ON = true` in it). Skip SCRIPT and STYLE text. And the two waiting
   listeners (`gamepadconnected`, `gamepaddisconnected`) are the ones PR9's bar 1 allows at load: allow exactly
   those two, nothing else.
10. **touch's frame count isn't matched.** The no-pad run steps 20 + 20 frames before its taps; a run with presses
    steps 20 + 3 per press + 4 per press + (20 - 6 per press): one or two frames more, so the clock is 0.02-0.04 min
    on, the crew have moved, and every picture differs, switch off or on. Step the same total in every run (or step
    the no-pad run through the same frame count with no presses). LB then RB also turns the view twice (geometries
    339 -> 357, textures 32 -> 34: the game builds a turned view's walls), so it can't equal a run that never turned:
    compare it with a no-pad run that presses Rotate the same way, or drop it.
11. **Mode (b) and the hand-back listeners (CT1's, small).** With a pad present at load, `gamepadconnected` fires
    before any press and `padHello` adds the hand-back listeners (pointerdown, wheel, mousemove +1 each). They do
    nothing until the pad is used (`padUnuse` returns when not used), so nothing changes for the player; but the hard
    rule is "nothing until a press". Suggest `padListen()` on the first `padUse()` instead of at the hello; then
    mode (b) is fully identical and the check can keep counting listeners.

## Paused (2026-10-22 06:02, lead 26: the 06:00 pare-down)
Where it stands: early notes 1-11 on CTT's controller_check sent to CTT, CT1, lead 26; no P3-P5 branch had landed. On waking: fetch claude/controller-p3..p5 and claude/controller-tests, re-run CTT's parts on the switch-on copy, then the per-package round above.
