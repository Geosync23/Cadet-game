# Review: fresh-eyes batch 2 (RV8)

Reviewer RV8 (session_01Q6uHYWus4ncyEgqWEYhJh5), for lead 29. Base for all: claude/arrows-c 6610dc7. Probes in
plans/review-rv8/ (run: `python3 p_x.py GAME.html DIR_WITH_cadet_test.py OUT`).

## CP4: claude/fe2-tracked 251d9788 (items 24 and 41): PASS

What changed: section 15b's Tracked only (trkItems marks `later`, trkFollowKey, TRK_SAID / trkSaid, trkTap, the panel's
and the device app's rows), interactions_check's new part, a build-table row. Nothing else.

- **24, a row for tomorrow.** Real taps at 390x844, Day 2 18:00: tapping "Breakfast, Tomorrow" in the Tracked panel sets
  no arrow, the panel stays open and the row reads "Tomorrow · the mess, Deck 3 · That's tomorrow: track it on the day".
  The same tap in the device app: no arrow, the device stays open, same words. On the base the same tap set an arrow to
  the mess hall for now and closed the panel. Today's rows still set their arrow.
- **41, the row the arrow follows.** With the round's arrow put up the way the round guide does (no Tracked tap), the
  job board row is lit with "ARROW" in the panel and "The arrow points here" in the device app; a tracked row still says
  "Tracking". No arrow: nothing lit.
- interactions_check: OK on the tip; on 6610dc7 with the tip's check, exactly the three new lines FAIL.
- check_fast on the tip: QUICK CHECK OK (161 s).
- cadet_test strictly alone, 6610dc7 vs tip: ALL IDENTICAL, no errors.
- Word note (not blocking, writer's call): "Tomorrow · ... · That's tomorrow: track it on the day" says tomorrow twice;
  "track it on the day" alone after the existing "Tomorrow ·" would do.

## DS1: claude/fe2-player 88df5899 (game commit 418ff167; item 27): PASS

What changed: one line in section 15's actBegin (the description is left out when the words already hold it),
player_check's new lines, a build-table row. Nothing else.

- Real screen tap on Deck 3's Long table at 390x844, Day 2 18:05, no tray (p_seat.py): the card reads "Seats eight. The
  engineers take this one ... You sit down. To eat, queue at the servery ..." once; card 694-826 px of 844, inside the
  screen. On 6610dc7 the description was there twice (card 672-826).
- player_check: OK on the tip; on 6610dc7 with the tip's check, exactly "the table's words should show once" FAILS.
- check_fast on the tip: QUICK CHECK OK (148 s). cadet_test strictly alone vs 6610dc7: ALL IDENTICAL, no errors.
- Note (not blocking): player_check runs at 900x760, so its "card fits the screen" line is not the phone size the user
  asked about; my phone-size tap above covers it for this review. The card fitted on the base too (bottom 826 of 844);
  the change makes it 22 px shorter. #25 (showering outside the cubicle) was not changed (DS1: not a bug, lead 29's call).
