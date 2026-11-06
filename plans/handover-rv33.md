# Handover: RV33 (reviewer, 0.99.7)

Session session_01GKuymoAK9gACR31MRd1CMX, reports to lead 49 (session_01GKuymjjreuZtZeDMBX79xn). Build master BM25 =
session_01GKuymnYTNkfxgLvtfFRg7w (the old BM24 session renamed): copy it on every PASS. Branch claude/review-rv33 (notes
plans/review-rv33.md, probes plans/rv33-probes/). Never edit the game on this branch.

## Verdicts sent (all with commit + game sha256 in review-rv33.md)
- SC1 social: PASS 77e573f (6df22594...1705).
- AV1 sound and screens: PASS 15fbf3f (4f081164...d5b2).
- TB6 hosted traditions: PASS 53bf2ce, carried to batch B 7b8a061 (83d08536...04aa7).
- EV1 new events: PASS dad2b9b, carried to 286ed5e and af18afd (72de6c46...c953).
- CL1 calendar: PASS bb26552 (b2ab09ae...8e69).
- SC1 words for TB6: PASS ab0e13e (0a100c8e...8344).
- JB3 jobs (taken over from RV32): PASS 1bbed58 with 35ab083 (352656bf...4c54).
- GM1 moved to SC1 by the lead.
## In progress
- Nothing. JB3 PASS sent (1bbed58 with 35ab083, game 352656bf...4c54). Idle.
- (was:) - JB3 35ab083 (JB3_FOOD_ON) + 1bbed58 (machine_check 5v), game 352656bf...4c54, taken over from RV32 (stopped). Plan and
  test build in review-rv33.md ("JB3 ..."): /tmp/rv33/jb3/run.sh (results m_*.txt, f_all_on.txt, d7_all_on.txt,
  cadet.txt, fast_off.txt). Verdict to JB3 (session_01GKuymmiCEm3CMMrMTdWMEo), BM25 and the lead.
  Expect: m_all_nofood FAIL food runs; m_all_on OK; m_food_* OK; m_planted FAIL "the ship meters: your jobs".

## Findings worth knowing
- machine_check "food runs in live play" is a knife-edge in 0.99.6: any change in who goes where in week 1 (CL1, EV1's
  LIGHT or SAT, TB6, MV1 RECWC) tips Sunday's (Line day) 16:00 meals run past the 2 h limit. JB3_FOOD_ON is the fix.
- The ship-meters "your jobs" line: jobs finished with no upkeep left show no meters; JB3's 5v counts them as nothing to show.
- Each builder ran check_fast with switches OFF; run it (and machine/device/food/join) with switches ON too.

## Gotchas
- stories_check needs `36` (backlog BM22-1). cadet_test's globals: don't name a probe variable HOOK (it replaces the
  harness's start-up code). The chat card is position:fixed (no offsetParent filter); a card away from the person closes.
- newGameStart(true) needs the manifest signed (form input[maxlength="24"], then the form button).
- skipTo can't go back in time; a probe that jumps back silently stays put.
- A toast logged twice 2 ship minutes apart is guideToast's queue, not a duplicate.
- Background runs over 3 h are killed: split long queues.
- Kit: pip install playwright numpy pillow; three r128 and acorn 8.12.1 in /tmp/cadet-work; CADET_CHROME=/opt/pw-browsers/chromium;
  give each parallel run its own CADET_WORK (with three/ and acorn/ symlinked).
