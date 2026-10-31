# 0.99.5 full round: runner R1

- NEW: `claude/staging-0995` e00bfabd, game sha256 `93aed54fa9296e75c308ae199cbac32465c776c650161fe41bf22535839a5164` (matched the GO; lead 48 confirmed that the earlier 5733867d number no longer applies). Then `claude/staging-0995` cc18dad0 (RV30's arrows_check fix, check only, the same game file, sha256 matched) for arrows_check.
- OLD: 0.99.4 `claude/staging-0994` 596712bc, game sha256 `a01d1a4c7864801b19541d70b9358089fba1ed84cee5145ca85931ea3012bc4a` (matched).
- BM23's GO 22:15 UTC 2026-10-31. Two browsers at most, each lane its own CADET_WORK (/tmp/work-r1, /tmp/work-r1-b); player_check alone at the end. R3 ran two OLD checks for me on its free browser (agreed, copied to BM23 and lead 48).

| Check | Result | Key lines |
|---|---|---|
| arrows_check (default parts), check from e00bfabd | FAIL (the check, not the game) | week: stuck at "Tap Chef Brennan to guess the spices"; "Unstick a gym locker" up over 3 h (see below) |
| arrows_check (default parts), check from cc18dad0 | OK | ARROWS CHECK OK (1617 s), week stuck 0 |
| arrows_check step5 | OK | ARROWS CHECK OK (418 s) |
| arrows_check step6 asis / teachoff / track / skiptea | OK x4 | ARROWS CHECK OK (824 s, one run) |
| arrows_check endstay | OK | ARROWS CHECK OK (962 s) |
| arrows_pointer_check | OK | arrows_pointer_check: OK (247 s) |
| player_check (alone) | OK | PLAYER CHECK OK (400 s) |
| bubble_check | OK | BUBBLE CHECK OK (784 s) |
| puzzle_check | **FAIL, NEW** (twice, the same) | cases were posted over Days 5-33 on paper: 0; p5's first: hidden: none |
| social_check | OK | SOCIAL CHECK OK |
| talk_check | OK | TALK CHECK OK |
| day_check 2 | OK | DAY CHECK OK |
| day_check 4 | OK | DAY CHECK OK |
| day_check 9 | OK | DAY CHECK OK |
| day_check 11 | OK | DAY CHECK OK |
| day_check 25 | OK | DAY CHECK OK |
| day_check 26 | OK | DAY CHECK OK |

## arrows_check week: the check's walker (fixed in cc18dad0)

With the arrows_check.py from e00bfabd, the "week" part (following only the arrow, Days 2-8) failed:

    FAIL week: stuck from Day 2 18:15 at "Tap Chef Brennan to guess the spices" (Deck 3) (fix: FX1 (arrows and tracking) or FX3 (the lift))
    FAIL week: the arrow "Unstick a gym locker" stayed up over 3 ship hours from Day 8 13:00 (fix: FX1 (arrows that never clear))

The other parts passed (queue, clockin, shift, promo, vessel). On OLD 596712bc (R3's run): week OK, stuck 0.
RV30 found both are the check's walker, not the game: it answered the spice supper's join arrow (TB3, new in 0.99.5)
with chatOpen instead of a real tap (a real tap joins at 18:17), and for the gym locker it tapped the treadmill and kept
working out ('gym' missing from its held-job list; a real floor tap at the stop starts the repair). RV30's 2-line fix to
the check, cc18dad0, was read and merged by BM23 into claude/staging-0995 (game file unchanged). With it: arrows_check
default parts OK, week Days 2-8 stuck 0.

## puzzle_check: NEW FAIL (repeats exactly)

On the candidate's game (93aed54f), twice, the same numbers each time:

    cases: 0; per rank: junior offered 2 rolled 0 posted 0; officer offered 1 rolled 0; senior 0; specialist offered 3 rolled 0; stats offered 6, rolled 0, posted 0
    FAIL cases were posted over Days 5-33 on paper: 0
    p5 first: {'staged': 'none'}
    FAIL p5's first: 3-pump-1's seal, slot 29, hidden: none

On OLD 596712bc (R3's run): PUZZLE CHECK OK; cases 1 (offered 10, rolled 1, posted 1: specialist); p5 first staged
creserve29:3-pump-1@24810 (seal), shown, fixed, closed. The sweeps (397 cases, P1-P4, p9) are fine on the candidate.
RV30's reading (sent to lead 48 and BM23): check fragility, not the engine. The paper run's count rests on 6-10 offers
(0.99.4 passes on a single case), and p5's first depends on the machine state earlier parts leave (run alone, the
candidate stages it and 0.99.4 doesn't); the sweep is identical. As the check stands it fails on every run of this
build (it runs on paper, so the same each time), so it's reported as NEW; lead 48 and BM23 decide how it is cleared.

**R1: FAIL on 0.99.5 (game 93aed54f): puzzle_check, NEW** (both of its FAIL lines, the same on every run; passes on
OLD). Everything else in the share is OK: 17 of 18 lines, arrows_check default parts with the fixed check from
cc18dad0, and player_check run alone with nothing else open.

## puzzle_check rerun with staging-0995 93839bf (RV30's paper-run line; check only, game 93aed54f unchanged)

Lead 48 asked for it on the candidate and on 0.99.4 (both with the puzzle_check.py from 93839bf, two browsers, each its own CADET_WORK):

| Game | Result | Lines |
|---|---|---|
| candidate 93aed54f | FAIL | the paper line passes now (cases 0 from 6 offers, no FAIL); still `FAIL p5's first: 3-pump-1's seal, slot 29, hidden: none` (p5 first: staged 'none') |
| 0.99.4 a01d1a4c | OK | PUZZLE CHECK OK; p5 first staged creserve29:3-pump-1@24810 (seal) |

So the paper line is cleared; p5's first is the one FAIL left (BM23 working on it).
