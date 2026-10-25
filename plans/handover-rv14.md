# Handover: RV14 (code reviewer), 2026-10-25 ~01:55 UTC

**Role:** reviewer under Lead 35 (session_01VQkkt8RXcvvGs1Dmzn2emM; was Lead 34). Notes-only branch `claude/review-rv14`;
full log `plans/review-rv14.md`. Never change the game. Verdicts to the builder, the lead and BM16
(session_01MB7n4yvCAeGyWN4WZCAGPh), with priority "next".

## Scope
0.92.5 item 16 (the weekend traditions; branch claude/p925-weekend) and item 19 (Cook-along in the galley).
Builders so far: FX14 -> FX11 -> FX9 -> DS1 -> now **FX16** (session_01MbKpntrDkcWAKrTj1HRUMm).

## Verdicts given
- Item 19 Cook-along in the galley: **PASS at 7ff6a818**. Merge note: needs bbcea5cb's evTagId 'cook' line and
  events_check's tagId 'cook' (6039daa2).
- Section 8c crewDetail swap line (80dff612, FX9's root cause of the Day 7 Pell hop): **PASS** (owner idle).
- 3e323170 (turn 1 + 4-week rotation): **PASS for its stage**.
- Told lead: food_check 7 'garden, good' is OLD (same numbers on ba836359); Day 62 observatory-night -4 vs 0.92.4 comes
  with FX12's merge (not the weekend).

## Final (2026-10-25 ~04:30 UTC)
- Item 16 switched ON: **PASS at 3307ded5** (game 49ba25a4...). Details in plans/review-rv14.md. Nothing open from me;
  the six-runner round is the lead's. perf_check weekend: flags expected (more people), told BM16.

## Earlier plan for the final verdict (done)
- The user (00:30/00:40 UTC): 0.92.5 ships the weekend SWITCHED ON, on a 4-week rotation; old weekend traditions keep
  days/times/places/hosts, lose at most 2 people, not below their floor (lead 35's rule).
- Wait for FX16's switch-on sha (seat-first line, T5 decor/head counts/perf, T6 birthday hour/records/design-doc).
- Then on the shipped file (switch ON as shipped): weekend_check, events_check, join_check, food_check 1 7, day_check 6,
  7, 14 (and 28), deck_check, check_fast, my plans/rv14-old_trads.py (BASE = the same build with WEEKEND_ON forced off;
  also vs 0.92.4 for information), cadet_test vs 0.92.4: only the expected weekend/FX12 differences (ask FX16 for the
  list), plants for any new check line (seat line: turn seat-first off).

## How I test
- Setup: plans/testing-guide.md 2.0 (playwright, three r128, acorn into /tmp/cadet-work). A worktree of the branch at
  /tmp/rv14/wk; builds in /tmp/rv14/b; each run its own CADET_WORK (/tmp/rv14/w-*) with three symlinked. Two browser
  runs at once; background commands need run_in_background and a timeout up to 2 h (the 30-min default kills them).
- Switch-on copy (while it ships off): sed "s/^const WEEKEND_ON = URL_FLAGS.has('weekend')/const WEEKEND_ON = true/".
  Once it ships on, the off copy is the reverse, for the old-traditions base.
- Running part of a check: take the file's text up to the first `with sync_playwright() as pw:` plus the part, set
  `__file__` to the real check's path (it execs cadet_test.py by replacing its own name).
- Gotchas: never pkill -f a pattern in your own command line (I killed my own background job that way). A weekend_check
  that "passed" for a builder once had never parsed: always run the check yourself. Vance is "he" in the game's words.

## Open questions for the user
None from me.
