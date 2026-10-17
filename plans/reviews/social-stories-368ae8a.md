# Re-review: claude/social-stories 31f8aea..368ae8a (0.39.4-0.39.5: goodbye moments, couples, moments ready for the writers' shapes)

Reviewer 1, 2026-10-17. Social B's own changes are in 20c; the section 20 hunks in this range are social A's 0.36.46 (already reviewed), merged in. name_check OK against 31f8aea. The WIP commits after 368ae8a (0.39.6, with social A's 0.36.57 merged) aren't reviewed yet.

**Verdict: PASS** (game code). The one social_check failure on the full merge is a social A test bug (below).

## Checked (full merge: arrival 4f6d0b2 + sim 971b4c7 + crew 98df62f + social A tip + social B tip + player-needs)
- **Couples are their own bond now:** bonds after the run are couple 4, best 11, friends 9, mentor 9, rivals 2. That fixes my earlier design note (couples counted as best friends).
- Goodbye moments take social A's goodbye slot. The "Coming and going" part gives the goodbye text from a moment ("Got a minute? There's something I need to tell you properly."), and the leaver's letters and "Moved on" still work.
- Save 23.0 kB (limit 30); save and load the same; the jump test True.

## For social A (its tip's social_check, 0.36.57): the purity test fails because the test itself creates a rel record
- On the full merge, `FAIL affBand, moodOf or purity wrong`. Diffing `socSave()` before and after the query block: the only change is `rel['torres-zeke']`, a new record `[0, null, null, ...]`.
- Cause: the beatOf test (social_check line 159) does `relGet(tz.id).arc = 2; ... relGet(tz.id).arc = 0;`. `relGet` creates a record for someone you haven't met (Torres here), and the test only resets `arc`.
- Fix: `const had = !!SHIP.rel[tz.id];` before, and `if (!had) delete SHIP.rel[tz.id];` after. No game change.
