# Review: claude/galley-food 812bedd (0.29.26: the traditions' meals, step 1: long breakfast and suppers)

Reviewer 1, 2026-10-17 (a new seat for me: galley engineer 3, session_018cicfPQZQXbxmtn6ygmL84). Diff against its base, combined 0.60.0 (e3ee66b): section 16 only (plus the build line), food_check.py, design-doc and DEV_NOTES. name_check OK.

**Verdict: PASS.** Two low notes; one item still owed.

## Checked
- **food_check OK** (rerun here), including the new long-breakfast case: pancakes, served to 10:00 (leftovers at 10:30); the chef cooks to 09:30, the early hand is on the line to 10:00.
- **day_check on day 6** (Saturday) OK: no short sleeps, meals or shifts, nothing double-booked, plans the same twice, draw calls peak 289. The Saturday breakfast wait (14 minutes, a slow oven) is the same on 0.60.0, so it isn't from this branch.
- The traditions' meals come from section 18's pure `tradTies('galley', d)` (guarded, with a test stand-in). `galleyPlan(role, d)` is the only reader of the shift plan, and the long breakfast shifts only the chef's and the early hand's mornings.
- The pie recolours its own cake mesh (its own `std()` material, through `col()`), with no candles, and only when the cake key changes. Nothing per frame.

## Low notes
1. **`GALLEY_TIES` caches by day only.** If a tradition with a galley tie is added for a day already cached (a one-off booked less than about a week ahead, when the galley board has already worked out this week's dinners), that day keeps the old menu for the session, and a reload would give the new one. Today's one-offs are safe (the farewells are booked 10 days ahead; Pell's show has no galley tie), but key the cache by an events signature (as `shipDay` does with `evSig`) to be sure.
2. **Breakfasts swapped:** Tuesday's pancakes swap with Saturday's spiced beans (`MENU.breakfast`), so every game's breakfast changes on two days. That's intended (pancakes for the long breakfast), but it's a visible game change for the lead's build notes.

## Still owed (the lead's note)
- The `galleyBirthdays` aboard() fix isn't in this commit.
