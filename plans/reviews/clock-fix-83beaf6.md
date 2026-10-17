# Review: claude/clock-fix 83beaf6 (on cand-0606 a775ea3), Works crew come early enough to clock in

Reviewer 1f, 2026-10-17. Builder: deck architect 3. A small schedule change, reviewed in full.

**Verdict: PASS.**

- **What changed:** the Works crew who use the time clock (`clocks`: Works, Deck 5, not nights, the clock place exists) end their morning `CLOCK_EARLY` = 7 minutes sooner, which covers the clock's queue wait (6) and the clocking (1). They're clocked in by 08:00 instead of queuing past it and working 535-539 of their 540 minutes. `clocks` is now worked out once per plan instead of inside `shiftWithBreaks`. The inputs are the same (`p`, `wd`, `S`), and day_check ran without errors, so there's no use-before-definition.
- **Effect:** the clocking crew's mornings are 7 minutes shorter (breakfast and wash end earlier), and they may start work a few minutes before 08:00. Nobody else's plan changes. cadet_test vs the candidate head: data and the crew-hidden shot are identical; only scheduled crew pixels move (Works crew sleeping on Deck 4 leave 7 minutes earlier), which is expected.
- **Evidence** (deck architect 3): day_check days 0, 6, 7 and 35 give shift short 0. Day 35's tray failure is fixed separately by poses 0.27.47 (8fef4ed, PASS). events_check OK.
