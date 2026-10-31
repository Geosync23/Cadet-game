# 0.99.4 full round: runner R1

- NEW: `claude/staging-0994` 8976965e, game sha256 `a01d1a4c7864801b19541d70b9358089fba1ed84cee5145ca85931ea3012bc4a` (matched).
- OLD: 0.99.3 `claude/integration` 57eceec4, game sha256 `04c821fe5619c9709f233be195c6cd5590c73d3caf81a106fc77bc1083a4c2a9` (matched).
- BM22's GO 06:29 UTC 2026-10-31. Two browsers at most, each lane its own CADET_WORK (/tmp/work-r1, /tmp/work-r1-b).

| Check | Result | Key lines |
|---|---|---|
| arrows_check (default parts) | OK | ARROWS CHECK OK (1706 s) |
| arrows_check step5 | OK | ARROWS CHECK OK (329 s) |
| arrows_check step6 asis / teachoff / track / skiptea | OK x4 | ARROWS CHECK OK (589 s, one run) |
| arrows_check endstay | OK | ARROWS CHECK OK (811 s) |
| arrows_pointer_check | OK | arrows_pointer_check: OK (218 s) |
| player_check | OK on rerun (first run FAILED, see below) | PLAYER CHECK OK (432 s, rerun) |
| bubble_check | OK | BUBBLE CHECK OK (674 s) |
| puzzle_check | OK | PUZZLE CHECK OK |
| social_check | OK | SOCIAL CHECK OK |
| talk_check | OK | TALK CHECK OK |
| day_check 4 | OK | DAY CHECK OK |
| day_check 11 | OK | DAY CHECK OK |
| day_check 25 | OK | DAY CHECK OK |
| day_check 26 | OK | DAY CHECK OK |

## player_check: one FAIL on the first run, not repeated (a check timing slip, not the build)

First run on 8976965e (lane B, /tmp/work-r1-b, alongside lane A's arrows_check in its own CADET_WORK; no other
player_check running):

    FAIL a v 1 save should load with needs at 80 (leisure 70, as new): [0, {'hunger': 60, 'energy': 100, 'hygiene': 60, 'fitness': 70, 'social': 70, 'bathroom': 60, 'leisure': 70}]
    FAIL a v 2 save should load its needs: {'hunger': 80, 'energy': 80, 'hygiene': 80, 'fitness': 80, 'social': 80, 'bathroom': 80, 'leisure': 70}

Each reload read like the step before it (the v 1 load showed a fresh game; the v 2 load showed what the v 1 load
should give), as if the page was read before the save had loaded. Reported to BM22 and lead 47 at once.

Proof it is not the build:
- player_check on OLD 57eceec4: PLAYER CHECK OK (515 s).
- The Saving part alone (player_check cut to its Saving section, nothing else changed): candidate twice OK, OLD once OK
  (v 1 save: day 2, needs 80, leisure 70, alarm 360; v 2 save: 11..66 kept).
- Whole player_check on the candidate again (/tmp/work-r1, one other browser): PLAYER CHECK OK, no errors.
- RV28 ran the whole player_check on 8976965e alone: PLAYER CHECK OK (plans/rv28-probes/player_8976965e.log on
  claude/review-rv28). RV28's reading: the Saving part's load() waits only for window.__sc, so on a busy host it can
  read a page too soon. Also noted by RV28: the Saving part writes a fixed page name (WORK/test/_save_check.html), a
  clash if two player_checks share a CADET_WORK (not the case here). Both are worth a backlog row for the check's owner.

**R1: OK on 8976965e** (14 of 14; player_check's one-off Saving FAIL did not repeat in four reruns on the candidate and passes on OLD).
