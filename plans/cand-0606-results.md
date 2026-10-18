# 0.60.6 check results

One line per finished check (check, game commit, OK/FAIL, key numbers). A new build master reruns only what is missing here.

- c20e8cd name_check OK · content_gen --check up to date (7515 lines) · smoke OK · newgame OK (Day 0 Sun 17:30 deck 5 manifest) · machine OK
- c20e8cd food_check FAIL: day 7 (Sunday) breakfast, salo-saad gave up waiting (152 came, 151 fed); garden 'missed 1' follows from it. Bisecting.
- c20e8cd cadet_test vs 7b57bb6: DIFFERENCES (state items/spots/calls; taps 0-4 + steers; toast = 0.28.41 need warning 'Very hungry'). Explaining step by step.
- a6ad933 (c20e8cd + poses 0.27.44-45) food_check OK (the day-7 miss gone with the washrooms reverted)
- c20e8cd deck_check OK (Deck 4 memory steady 373 geo / 39 tex) · leave_check OK
- c20e8cd day_check (R2): day 1 OK; days 0/6/7/35 FAIL: 'shift short' (2 crew 1-2 min under 540) + day 0/35 'standing still with a tray' once on Deck 3 (~18:00). Peak calls D3 277. Re-running on a6ad933 and bisecting.
- c20e8cd perf (perf 3): FAIL phone speed: dinner 6.1→9.2 ms, slow frames 29→279/h, breakfast worst 213 ms; cause poses 0.27.40 seatCushion ray (~9 ms). Calls peak 431, memory 150 flat. Fix pending (lead's call).
- c20e8cd lines PASS (0 err, 3 warn) · tiles ALL OK · arc OK · booth (arc 70 booth) OK · device FAIL 'no leak' 496→497 (poses 0.27.42 crowd change), device OK on b679455
- c20e8cd events FAIL: dayReport 'work' shift-short most days (= leave's time clock, clock-in wait, owner career engineer) + day 20 fonseca-arjun film 20:02-22:33. cadet_test diffs all explained per step (see DEV_NOTES row later).
- c20e8cd player (R3): FAIL one: cart run loading in the hold, player.holding 'cart' not 'cartfull' (bisecting) · interactions OK · path OK (2872/2872)
- a6ad933 day_check (R2) days 0/6/7/35: still shift short (leave clock, PE8); day 35 Deck 3 tray-still quist-ilse 17:59 (from poses ce1c84f, R2 bisect). intro_check started on b679455 (baseline).
- 0d8072c (+ poses 0.27.46, no seat ray) cadet_test vs b679455: data/taps/walks identical; one tap shot ~97k px that moves between runs (tip timing, real-time noise). intro_check on b679455 died (page-load timeout, busy machine): to re-run.
- 157c0dd (poses 0.27.46) phone.py (DA3) vs 0.60.5b: dinner 3.7-4.5 ms vs 3.6-4.0, >16.7 ms 6-17 vs 11; breakfast in range. Stutter fixed.
- player cart-run fail: not the hand-merged held-prop line (fresh-game cart run gives cartfull on 7b57bb6, c20e8cd, 0d8072c); R3 re-running player_check alone on 0d8072c. intro_check running on 0d8072c (alone).
- c707b5f = + poses 0.27.47 (day-35 tray fix, DA3-tested on 0d8072c: cadet_test identical, tray fail gone)
- d571db4 (+ player-needs 0.28.50, Put down 0.28.60): smoke OK · newgame OK · device OK · NAMES OK · content_gen up to date · cadet_test vs c707b5f: data/taps/walks identical, every shot ~15k px only in the top control bar (the Pause button, 0.28.48/50)
- d571db4 day_check (R2): day 0 FAIL only shift short 2 (clock fix pending), tray line gone; day 1 OK; peaks D3 277; servery 125/125, 128/128. R3: player cart-run fail repeats on 0d8072c (player_check alone); debug run on d571db4 in flight.
- faa2562 (+ clock-fix 83beaf6): events_check OK (no shift short, no film overrun)
- faa2562 day_check (R2) days 0/6/7/35 all OK: shift short 0, tray gone, stuck 0.0, peak D3 279
- d571db4 (R3): interactions OK · path OK (3093/3093) · player FAIL cart-run c2 = one-frame lag (holding follows stage next frame); test-only fix in player_check (step 1 before c2/c3) being verified on faa2562
- faa2562 + player_check cart fix (890a1f3): PLAYER CHECK OK (cart run cart → cartfull → cart)
- 2757963 (+ player-needs 0.28.56, putdown 1117454): tiles ALL OK · device OK · cadet_test vs 890a1f3 ALL IDENTICAL · NAMES OK · content_gen up to date
- 2757963 day_check (R2) days 0, 1 OK (peak D3 277)
- 0d8072c intro_check (busy machine): parts 0-11 OK, part 12 OK through d3-store, then stopped at the 2 h limit (slowness, 0 FAILs). Final intro = R4 alone on the final candidate.
- 2757963 (R3): player OK (cart fix works) · interactions OK · path OK (3008/3008)
- FINAL CANDIDATE 96582c4 (+ shuffle ec6e8a0). Final run started 00:50: R4 intro, R2 days 0/1/6/7/35, R3 player/interactions/path, DA3 phone+perf, BM3 the rest.
- 96582c4 BM3 share: NAMES OK · content_gen up to date (7515) · smoke OK · newgame OK · food OK · machine OK · deck OK · leave OK · device OK · lines PASS (0 err, 3 warn) · tiles ALL OK · events OK · arc OK · booth OK · social OK · cadet_test vs 2757963: only i_tap3 7014 px (shuffle-aside) · vs 0.60.5b: explained diffs (no place/spot changes now; walks/taps = player-needs time skip; Pause button; poses; bubbles)
- 96582c4 day_check (R2) days 0/1/6/7/35 ALL OK: shift short 0, stuck 0.0, peak D3 279 (budget 450), servery all served
