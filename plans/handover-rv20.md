# Handover: RV20 (Step 5 reviewer), 2026-10-26 ~23:50 UTC

**Role:** reviewer for Pillar 5 Step 5 (spec plans/p5-step5-spec.html on claude/p5-specs). Notes-only branch
`claude/review-rv20`; the full log and every verdict are in `plans/review-rv20.md` (its last section, "STOPPING POINT",
says exactly where each open review stands). Hired by lead 39; now lead 40 (session_01NXybH7NNqM8M4ngiyidq6m). Send every
verdict with the exact sha to the builder, lead 40 and BM18 (session_01A3S2VBMYmTt2wCZa8ej7XR). Other reviewer: RV21
(session_01AmTyMHLr5UuCY9zo3nQcwS; has B4 and B3's M20). When B5's promotion passes, tell lead 40 at once (an early Dev
link for the user).

## Verdicts
| Piece | Sha | Verdict |
|---|---|---|
| SW3 words | 277b9c15 | PASS |
| B2 M19 | 3c38a65f | FIXES NEEDED (all three since fixed in deefa61a, see open) |
| B4 P4/P5 | 55b2e6a8 | PASS |
| B4 board + turn 4 | 4e5c878f | PASS |
| B3 shutdowns | 5ad090ff | FIXES NEEDED (M1 teacher: B5's e7ff9253; M2, M3: B3's 9ab93abf, not reviewed) |
| B2 tap fix (0.93.4) | c79a66dc | PASS |
| EN1 careerOff hook | cd4196d5 | OK (one-line career review for lead 40 / RV21) |
Open: 9ab93abf (B3 shutdown fixes, not started). Done since: b7e84f81 PASS; deefa61a PASS for B2 (the build carries 51b1a9c6's machine_check FAIL); e7ff9253 FIXES NEEDED (that FAIL; shoulds S1-S4). See review-rv20.md, last section.

## Builders
B2 mechanics A session_015mjNkxuGoEZGKA2ksBPz9u (claude/p5s5-mech-a, claude/workstep-tap-fix); B3 session_014FBmsiTsA9QymoN2qt4NyL
(claude/p5s5-mech-b, claude/p5s5-m20); B4 session_01LV8Q8UV6aJPTgmQ6ub1z8G (claude/p5s5-puzzles); B5 session_01CgbXRamJJp66pFTP43KYoB
(claude/p5s5-promo; owns 24 core / 24u for Step 5 now); VB2 session_01KRBGtugjBpv5iGcV5WDvCP (claude/p5s5-kit). B1 and SW3 retired.

## How I test (and what bit me)
- Worktrees per sha under /tmp/rv20/; a switched-on copy by sed on the P5_STEP5 line; base for "off" = skeleton 5957d244
  (or the branch's own merge base: c79a66dc / acbb52e0 for builds carrying staging-0.93.3).
- Live probes (plans/rv20-*.py): exec cadet_test.py's top half (instrument, INIT, THREE), serve on 127.0.0.1, ?p5s5#dev,
  Dev "Set career to Day 13/14/15", then set the rest by hand (W.tier, W.rank, W.tr and W.op), devmodeSkipTo, real
  frames. Tap with page.mouse.click at a projected placeSpot (ixTap skips PLAYER_TAPS order). Meeting cards: click
  button.act. A Dev clock jump replays queued lines (don't judge repeats after one). A test's player may have tracking off.
- Every CADET_WORK needs three/ and acorn/ (check_fast's names step dies at once without acorn). At most 2 browsers at once.
- Don't pkill with a pattern that appears in your own command line (it kills your shell).

## Open questions for the user
None from me.
