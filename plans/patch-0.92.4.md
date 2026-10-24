# Patch 0.92.4: the user's answers to the 0.92.3 morning summary (2026-10-24 ~14:10 UTC, 10:10 AM Eastern)

Base: claude/integration 3866c8f3 (0.92.3, game sha256 f18e8540…7853). Each builder branches from it, runs its area checks + cadet_test, pushes, sends the sha to its reviewer and BM16 (staging claude/staging-0.92.4). Then the full six-runner round, lead's go, PUB1 publishes 0.92.4 as an update of the 0.92.3 NEW pages (3HqM5…, 9ZWAg…): the user decided 15:08 UTC.

| # | The user's answer | Who | Reviewer |
|---|---|---|---|
| A | Trays: NOT travelling. The tray goes away when you get up from the table. If you never sit down, it disappears when you leave the mess hall. Only exception: the pick-your-own breakfast tray (it travels to the mess). TRAY_TRAVELS off, plus: get-up from a mess seat clears the tray; leaving the mess hall without sitting clears it; pick-your-own tray keeps travelling until eaten at a seat. Update design-doc. | FX12 | RV12 |
| B | Dirty clothes Day 1: keep the NEW green tip; drop the old "Yesterday's clothes" pop-up (it wasn't firing for the user anyway); add another reminder the next day if still in yesterday's clothes. | FX4 | RV11 |
| C | Yes: smooth the ~0.7-tile hop when crew get up from a place (all crew, section 10). | FX8 | RV11 |
| D | Yes: warn when you take a repair job whose part would run past the start of a lesson. | FX10 | RV13 |
| — | Needs pace: the user will test and report. Bedtime tip, pick-your-own toast, dinner heads-up: keep as is. | — | — |
| — | Sim bay plan (https://claude.ai/artifact/Hmg44se58wGkZaGCMFyRWL): still waiting for the user's answers. | FX14 idle | — |
