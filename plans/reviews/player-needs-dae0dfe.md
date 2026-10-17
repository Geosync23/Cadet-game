# Re-check: claude/player-needs 0.28.49 (dae0dfe), tradition posts name the tradition

Reviewer 1f, 2026-10-17. Builder: player engineer 5. A re-check of 1e's MEDIUM (player-needs-f2c2f81.md), plus the small changes alongside it.

**Verdict: PASS.** 1e's MEDIUM is fixed. There are two LOWs, pre-existing or cosmetic, for later. 0.28.47 is covered by 1e's 48f66e8 review and 0.28.48 by mine (player-needs-2e69a13.md, PASS WITH FIXES: its MEDIUM goes to PE6's follow-up).

## Checked
- **The fix.** `newsTrad` and the 'tradition' note pass `{ trad: name (lower case), tradId: id }`. Section 22's `lineCond` 'trad' also matches `ctx.tradId`, so the bank's `? trad:quiz` lines still match. The 'today' condition still reads `!!ctx.trad`. The name comes from `eventsOn(d)`, with the id with spaces as a fallback.
- **Probe** (`player-needs-dae0dfe-trad-probe.py`): claude/content's `news.lines` baked in, with player-needs' own `content/`, `content_gen.py` and `trad_parse`. It fires the 'tradition' note for every one of the 30 traditions and ticks the feed every ship minute for four weeks (55 'today' posts). **No post contains an event id.** The only match was "hull-lights evening", which is the tradition's real name. 1e's news probe isn't needed again: the feed's pacing code is unchanged.
- **Social cap.** `+min(20, 12 × bb)` per tradition. Fine.
- **t:rep.** `TEACH_ST.turnin` is now a ship-minute stamp, set once. `TEACH_ST` isn't saved, so there's no old-save `true` to worry about. The tip waits 30 ship minutes after your first turn-in, or comes at 17:00 / on day 2 as before.
- **PE5's checks:** player_check, interactions_check and lines_check PASS; cadet_test vs 0.28.48 ALL IDENTICAL. That fits the diff (no Deck 4 or start-state change), so I didn't rerun them.

## LOWs (for later, not blocking)
1. **Lower-casing breaks proper names:** "It's brennan's tasting table today." Fix: lower-case only the first letter, and only when the first word isn't a crew name. Or give traditions a `short` name for lines to use.
2. **Pre-existing (since 0.28.44):** a "done" post (`trad.done.<id>`) also picks the bank's `trad:today` lines and the untagged filler. So just after a tradition you can read "A ship tradition today: long breakfast. Turn up and join in." or, after book circle, "Running club tonight…". 17 of the 30 traditions get no done post at all, which is fine (nothing fits). Fix, when the writers add `trad.done` lines: have done posts use only lines with a `flag:trad.done.*` or `trad:<id>` condition.
