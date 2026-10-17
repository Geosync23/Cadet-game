# Review: galley 0.29.36 (7b81f4a), a taste is a quarter of a meal unit

**Reviewer:** adversarial reviewer 2b. **Verdict: PASS.**

- The tasting table now cooks `ceil(tastes / FOOD.tastes)` meal units (4 tastes each, produce first, then the cold
  store) and lays out at most the tastes asked for (`got = min(n, units * 4)`); still two tastes per planned taster.
  `st.tastes` counts tastes and `st.fresh` counts produce units, as their names say.
- On the trial merge (galley 7b81f4a + sim e1bb1e6 + ship-events): **machine_check OK**, "Food runs in live play, 6
  days: runs 5, late [], cold store low 133" (the sixth Thursday run is gone); **food_check OK** (7b81f4a's).
- cadet_test 0.29.35 vs 0.29.36: **ALL IDENTICAL**.
