# Review: claude/social-fixes d449914..d651ad6 (0.62.0-0.62.2: no promenade trestle, Letters evening scratched, one call home a day, one-sided calls with no repeats)

Reviewer 1c, 2026-10-17. Diff: `git diff d449914 d651ad6` (section 3's deck data and decor, section 20c, the baked traditions and home calls, the checks). Tested on the branch head.

**Verdict: PASS** (two lows).

## Checked
- **social_check: OK. events_check: OK** (its tradOn case now uses sunday-table).
- **Calls home, a 60-day probe** (one call a day at 19:00, rotating mum/gran/jo/sam, each heard to the end):
  - **one a day:** after each call, `homeCallable` is empty and a second `homeScript` returns null, every day;
  - **no repeats:** each contact had 15 calls, 6-7 beats and 8-9 scenes, all different (no scene repeated);
  - **save:** the home part grew to 1,806 bytes by day 60. `c.h` is capped at 16 tags a contact (9 used here).
- **Old saves:**
  - `c.sent` and `c.last` are kept but unused;
  - the new `H.call` is undefined on an old save, which reads as not called today;
  - the first-call text is keyed on any `c.day`, so a player who called before never sees "Your first call home".
- **The booth:** once a call is queued, `onPick` returns at once (`if (call) return`). With no choices left in calls, nothing can be picked twice.
- **The trestle and the Letters evening:**
  - the promenade tiles [25..27,10] are no longer blocked;
  - `3-longtable-1..4` are the four mess end chairs;
  - nothing in this build refers to `homeLive`, `homeSends`, `3-postbox-1` or `3-longtable-5+` any more;
  - other branches still carry the old `3-postbox-1` place and a `tradOn('letters')` comment, as unchanged shared lines; a merge takes this branch's removal, and `tradOn('letters')` simply returns false.

## Low
1. **A contact with nothing to say is still offered.** On day 10 of the probe, Jo had no beat due and no scene fitting the day, so `homeScript('jo')` returned null. The booth still lists "Call Jo", and picking it just ends the panel without a word. Today's call isn't used up, so nothing is lost, but it looks broken. Fix: list only contacts with `homeLines(k, t)` not null, or give a line ("Jo's not picking up. Try tomorrow.").
2. **`c.news` has no hard cap.** It holds one tag per news scene ever heard, bounded today only by how much news content exists. The save rule asks for a hard bound and its worst case in DEV_NOTES' Save bounds: cap it (e.g. `slice(-32)`) and write the worst case next to `c.h`'s 16. Today's measured total is 1.8 KB at day 60, well inside the social budget.

## 0.62.3 (3960b06), skimmed (content only)
- Only `content/home/*.call` and their baked lines in the game changed, plus the build line. No code changes. The engineer reports arc_check (calls and arcs) OK and lines_check PASS. **PASS.** The longer scenes may also make low 1 (a contact with nothing to say) rarer, but the guard is still worth having.
