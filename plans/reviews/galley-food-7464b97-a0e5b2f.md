# Review: galley 0.29.35 (7464b97) and food_check a0e5b2f

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS** (both).

## food_check a0e5b2f (test only)
- With section 10's live line, the check now takes everyone else out of the line (`lineLeave`), starts your serve
  (`galleyTurn`) and moves on one serve (`GALLEY_SERVE.you`); without the line it uses `turnAt` as before. It still
  checks "not your turn too soon" first. It no longer tests the turnAt estimate when the line is live, which is right:
  there turnAt is only a guess.
- On galley + sim e1bb1e6 (0.26.37) + ship-events: `[1, False, True, True, False, True]`, **FOOD CHECK OK** (with
  0.29.35 merged). On 0.29.34 html this food_check fails its new one-off check, as expected (that check belongs to 0.29.35).

## galley 0.29.35 (7464b97): day caches follow the day's events
- `galleyTies(d)` keeps a signature of `eventsOn(d)` (each event's id and times); when it changes, that day's ties,
  tasting, rota and day events are dropped and all menus cleared, then worked out again. By content, so a list made
  again the same keeps the caches. Tests set `GALLEY_TEST.tradTies` and skip it.
- food_check's new case on the merge: a late one-off (day 43) appears in the galley's day (`galley-test@1080-1140`)
  and goes again when removed.
- Cost: in play at Sunday dinner, galleyTies runs about 0.11 times a frame (eventsOn 0.27), so the extra signature
  string is nothing.
- cadet_test 0.29.34 vs 0.29.35: **ALL IDENTICAL**.
